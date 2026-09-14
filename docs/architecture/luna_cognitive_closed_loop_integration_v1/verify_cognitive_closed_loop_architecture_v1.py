"""V0 static verifier for Luna Cognitive Closed Loop Integration.

Planning Only: validates the global cycle, interaction/state/feedback/trace
contracts and failure matrix without importing or executing Runtime, Model,
Hardware, Provider, Action, or online-learning code.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "global_cognitive_loop_contract_v1.json",
    "cognitive_cycle_lifecycle_v1.json",
    "module_interaction_matrix_v1.json",
    "global_state_integration_contract_v1.json",
    "decision_action_feedback_loop_v1.json",
    "expectation_difference_contract_v1.json",
    "feedback_integration_contract_v1.json",
    "role_emotion_action_integration_boundary_v1.json",
    "cognitive_trace_lifecycle_v1.json",
    "failure_scenario_matrix_v1.json",
    "closed_loop_runtime_interface_v1.json",
    "closed_loop_cognitive_core_interface_v1.json",
    "closed_loop_capability_interface_v1.json",
    "closed_loop_dependency_boundary_v1.json",
)
MD_ASSETS = (
    "luna_cognitive_closed_loop_architecture_v1.md",
    "closed_loop_whitebox_v1.md",
    "closed_loop_go_no_go_v1.md",
)


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

    loop = data.get("global_cognitive_loop_contract_v1.json", {})
    lifecycle = data.get("cognitive_cycle_lifecycle_v1.json", {})
    matrix = data.get("module_interaction_matrix_v1.json", {})
    state = data.get("global_state_integration_contract_v1.json", {})
    feedback_loop = data.get("decision_action_feedback_loop_v1.json", {})
    difference = data.get("expectation_difference_contract_v1.json", {})
    feedback = data.get("feedback_integration_contract_v1.json", {})
    role_emotion = data.get("role_emotion_action_integration_boundary_v1.json", {})
    trace = data.get("cognitive_trace_lifecycle_v1.json", {})
    failure = data.get("failure_scenario_matrix_v1.json", {})
    runtime = data.get("closed_loop_runtime_interface_v1.json", {})
    core = data.get("closed_loop_cognitive_core_interface_v1.json", {})
    capability = data.get("closed_loop_capability_interface_v1.json", {})
    boundary = data.get("closed_loop_dependency_boundary_v1.json", {})

    required_stages = ["Observe", "Context Formation", "Attention Allocation", "Situation Understanding", "Hypothesis / Belief Update", "Expectation Comparison", "Brain Evaluation", "Decision Commitment", "Action Boundary", "Action Runtime", "Outcome Collection", "Learning Update", "Memory Consolidation", "Next Cycle"]
    check(loop.get("stages") == required_stages, "global_loop_stages")
    check(loop.get("entry") == "Runtime Foundation Tick/Wake-up Candidate", "global_loop_entry")
    check(loop.get("exit") == "Memory and Learning Update Candidate", "global_loop_exit")
    check(loop.get("rules", {}).get("runtime_manages_cycle") is True, "loop_runtime_managed")
    check(loop.get("rules", {}).get("cycle_not_infinite_automatic") is True, "loop_not_infinite")
    check(loop.get("rules", {}).get("stage_trace_required") is True, "loop_trace_required")

    check({"Created", "Activated", "Processing", "Decision Pending", "Action Pending", "Feedback Waiting", "Learning", "Completed", "Archived"}.issubset(set(lifecycle.get("states", []))), "cycle_lifecycle_states")
    check({"cycle_id", "start_time", "current_stage", "active_modules", "trace_id"}.issubset(set(lifecycle.get("schema", []))), "cycle_lifecycle_schema")
    check(len(lifecycle.get("transitions", [])) >= 7, "cycle_lifecycle_transitions")
    check(lifecycle.get("rules", {}).get("state_owner_required") is True, "cycle_state_owner")

    rows = matrix.get("rows", [])
    modules = {row.get("module") for row in rows}
    check({"Field", "Attention", "Brain", "Memory", "Learning", "Emotion Context", "Capability", "Action Runtime"}.issubset(modules), "interaction_modules")
    check(all(row.get("input") and row.get("output") and row.get("read") is not None and row.get("write") is not None and row.get("permission") for row in rows), "interaction_io_permission")
    check(matrix.get("rules", {}).get("input_output_required") is True, "interaction_input_output_rule")
    check(matrix.get("rules", {}).get("cross_layer_direct_call_forbidden") is True, "interaction_cross_layer_guard")

    check({"Field State", "Self State", "Workspace State", "Memory State", "Attention State", "Capability State", "Action State", "Emotion Context", "Role Context"}.issubset(set(state.get("components", []))), "global_state_components")
    check({"global_state_id", "timestamp", "components", "snapshot_version"}.issubset(set(state.get("schema", []))), "global_state_schema")
    check(state.get("rules", {}).get("composes_only") is True, "global_state_composes_only")
    check(state.get("rules", {}).get("does_not_own_components") is True, "global_state_not_owner")

    check(feedback_loop.get("pipeline") == ["Decision", "Action Candidate", "Validation", "Execution Future", "Outcome", "Expectation Difference", "Learning Signal"], "decision_feedback_pipeline")
    check({"Expectation", "Memory", "Learning"}.issubset(set(feedback_loop.get("required_reentry", []))), "decision_feedback_reentry")
    check(feedback_loop.get("rules", {}).get("action_boundary_required") is True, "decision_action_boundary")
    check(difference.get("schema") == ["expected", "actual", "difference", "confidence", "learning_candidate", "trace_id"], "expectation_difference_schema")
    check(difference.get("rules", {}).get("not_prediction") is True, "difference_not_prediction")
    check(difference.get("rules", {}).get("reality_feedback_required") is True, "difference_reality_feedback")

    check({"External Feedback", "Social Feedback", "Internal Feedback"}.issubset(set(feedback.get("feedback_types", []))), "feedback_types")
    check({"Learning", "Memory", "Role Evolution Candidate"}.issubset(set(feedback.get("consumers", []))), "feedback_consumers")
    check(feedback.get("rules", {}).get("learning_candidate_only") is True, "feedback_candidate_only")

    check(role_emotion.get("pipeline") == ["Field Event", "Role Activation", "Emotion Context", "Brain Evaluation", "Decision", "Action Boundary", "Outcome", "Emotion Update Candidate"], "role_emotion_pipeline")
    check("Emotion → Direct Action" in role_emotion.get("forbidden", []), "role_emotion_action_guard")
    check(role_emotion.get("rules", {}).get("context_only") is True, "role_emotion_context_only")
    check(role_emotion.get("rules", {}).get("no_direct_action") is True, "role_emotion_no_action")

    check({"Cycle Start", "Evidence", "Context", "Attention", "Belief", "Expectation", "Decision", "Action", "Outcome", "Learning", "Cycle End"}.issubset(set(trace.get("stages", []))), "trace_stages")
    check({"trace_id", "cycle_id", "stage", "reference", "timestamp", "owner", "provenance"}.issubset(set(trace.get("schema", []))), "trace_schema")
    check(trace.get("rules", {}).get("provenance_required") is True, "trace_provenance")
    check(trace.get("rules", {}).get("cycle_end_required") is True, "trace_cycle_end")

    cases = {case.get("case") for case in failure.get("scenarios", [])}
    check({"Capability Error", "Action Failure", "Role Conflict", "Emotion Context Increase"}.issubset(cases), "failure_cases")
    check(all(case.get("path") and case.get("output") for case in failure.get("scenarios", [])), "failure_paths")
    check(failure.get("rules", {}).get("unknown_preserved") is True, "failure_unknown")
    check(failure.get("rules", {}).get("failure_not_silent") is True, "failure_not_silent")

    check({"Tick", "Wake-up", "Process", "State Synchronization", "Trace", "Recovery"}.issubset(set(runtime.get("runtime_provides", []))), "runtime_interface")
    check({"Constitution", "Governance Authority", "Decision Ownership", "Reality"}.issubset(set(runtime.get("runtime_not_modified", []))), "runtime_boundary")
    check(runtime.get("rules", {}).get("runtime_owns_timing") is True, "runtime_owns_timing")
    check(runtime.get("rules", {}).get("no_real_loop") is True, "runtime_no_real_loop")

    check({"Evidence", "Field Context", "Self Context", "Attention", "Memory Retrieval", "Expectation Feedback"}.issubset(set(core.get("core_inputs", []))), "core_interface_inputs")
    check({"Situation", "Hypothesis", "Brain Input Package", "Decision Commitment", "Learning Candidate", "Memory Candidate"}.issubset(set(core.get("core_outputs", []))), "core_interface_outputs")
    check(core.get("rules", {}).get("brain_owns_judgment") is True, "core_brain_judgment")
    check(core.get("rules", {}).get("closed_loop_not_brain") is True, "loop_not_brain")

    check({"Capability Requirement", "Observation Requirement", "Priority", "Resource Constraint"}.issubset(set(capability.get("loop_inputs", []))), "capability_interface_inputs")
    check({"Evidence Candidate", "Capability Health Candidate", "Failure Candidate", "Performance Evidence"}.issubset(set(capability.get("capability_outputs", []))), "capability_interface_outputs")
    check("Cognitive Loop Ownership" in capability.get("capability_not_own", []), "capability_no_loop_owner")
    check(capability.get("rules", {}).get("capability_does_not_initiate_loop") is True, "capability_no_initiate")

    forbidden = set(boundary.get("forbidden", []))
    for item in ("Closed Loop → Constitution Modification", "Closed Loop → Direct Reality Modification", "Capability → Cognitive Loop Ownership", "Emotion → Direct Action", "Learning → Automatic Value Rewrite"):
        check(item in forbidden, f"dependency_guard:{item}")
    check(len(boundary.get("allowed", [])) >= 5, "dependency_allowed_edges")
    check(boundary.get("rules", {}).get("loop_is_coordination_not_authority") is True, "dependency_not_authority")
    check(boundary.get("rules", {}).get("feedback_reentry_required") is True, "dependency_feedback_reentry")
    check(boundary.get("rules", {}).get("no_runtime_execution") is True, "dependency_no_runtime")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
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
    print("READINESS: LUNA_COGNITIVE_CLOSED_LOOP_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
