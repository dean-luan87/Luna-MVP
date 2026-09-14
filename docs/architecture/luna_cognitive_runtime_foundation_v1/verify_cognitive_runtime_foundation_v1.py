"""V0 static verifier for Luna Cognitive Runtime Foundation contracts.

Planning Only: no Runtime loop, Scheduler, thread, async, provider, device,
or Action code is imported or executed.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "runtime_foundation_layer_definition_v1.json",
    "runtime_loop_contract_v1.json",
    "runtime_tick_system_contract_v1.json",
    "runtime_wakeup_contract_v1.json",
    "runtime_event_processing_contract_v1.json",
    "runtime_state_synchronization_contract_v1.json",
    "runtime_snapshot_contract_v1.json",
    "runtime_trace_integration_contract_v1.json",
    "runtime_failure_recovery_contract_v1.json",
    "runtime_persistence_boundary_v1.json",
    "runtime_os_interface_contract_v1.json",
    "runtime_cognitive_core_interface_v1.json",
    "runtime_dependency_boundary_v1.json",
)
MD_ASSETS = (
    "luna_cognitive_runtime_foundation_architecture_v1.md",
    "runtime_whitebox_v1.md",
    "runtime_go_no_go_v1.md",
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

    layer = data.get("runtime_foundation_layer_definition_v1.json", {})
    loop = data.get("runtime_loop_contract_v1.json", {})
    tick = data.get("runtime_tick_system_contract_v1.json", {})
    wake = data.get("runtime_wakeup_contract_v1.json", {})
    event = data.get("runtime_event_processing_contract_v1.json", {})
    sync = data.get("runtime_state_synchronization_contract_v1.json", {})
    snapshot = data.get("runtime_snapshot_contract_v1.json", {})
    trace = data.get("runtime_trace_integration_contract_v1.json", {})
    recovery = data.get("runtime_failure_recovery_contract_v1.json", {})
    persistence = data.get("runtime_persistence_boundary_v1.json", {})
    os_interface = data.get("runtime_os_interface_contract_v1.json", {})
    core_interface = data.get("runtime_cognitive_core_interface_v1.json", {})
    boundary = data.get("runtime_dependency_boundary_v1.json", {})

    required_children = {"Runtime Loop", "Tick System", "Wake-up System", "Event Processing", "State Synchronization", "Snapshot Management", "Runtime Trace", "Failure Recovery", "Persistence Boundary", "OS Interface", "Cognitive Core Interface"}
    check(layer.get("layer") == "L1 Runtime Foundation", "foundation_layer")
    check(required_children.issubset(set(layer.get("children", []))), "foundation_subsystems")
    check(layer.get("rules", {}).get("contract_only") is True, "foundation_contract_only")
    check("Decision ownership" in layer.get("not_authority", []), "foundation_no_decision")

    check(loop.get("sequence", [])[0:3] == ["Wake-up", "Collect Pending Event", "Update Runtime Context"], "loop_sequence_prefix")
    check({"runtime_loop_id", "trigger", "input", "output", "state_change_allowed", "action_allowed"}.issubset(set(loop.get("schema", []))), "loop_schema")
    check(loop.get("constraints", {}).get("state_change_allowed") is False, "loop_no_state_write")
    check(loop.get("constraints", {}).get("action_allowed") is False, "loop_no_action")
    check(loop.get("constraints", {}).get("decision_direct") is False, "loop_no_decision")

    check(set(tick.get("tick_types", [])) == {"System Tick", "Cognitive Tick", "Event Tick"}, "tick_types")
    check({"tick_id", "priority", "scope", "trigger", "timeout", "interruptible"}.issubset(set(tick.get("schema", []))), "tick_schema")
    check(tick.get("rules", {}).get("tick_not_action") is True, "tick_no_action")
    check(tick.get("rules", {}).get("real_scheduler_out_of_scope") is True, "tick_no_scheduler")

    check(set(wake.get("sources", [])) == {"External Wake-up", "Internal Wake-up", "Reflex Wake-up"}, "wakeup_sources")
    check({"wake_id", "source", "priority", "reason", "target_process"}.issubset(set(wake.get("schema", []))), "wakeup_schema")
    check(wake.get("rules", {}).get("high_priority_may_interrupt") is True, "wakeup_priority")
    check(wake.get("rules", {}).get("wake_up_not_action") is True, "wakeup_no_action")

    check(event.get("pipeline", [])[0:3] == ["Event", "Validation", "Classification"], "event_pipeline")
    check(set(event.get("event_classes", [])) == {"External Event", "Internal Event", "System Event", "Reflex Event"}, "event_classes")
    check({"event_id", "source", "timestamp", "target", "payload", "trace_id"}.issubset(set(event.get("required_fields", []))), "event_schema")
    check("Event → Action" in event.get("forbidden", []), "event_no_action")
    check(event.get("rules", {}).get("validation_before_route") is True, "event_validation_first")

    check(sync.get("pipeline") == ["Module Output", "State Proposal", "Owner Validation", "Reducer", "New State"], "sync_pipeline")
    check({"sync_id", "state_id", "source_module", "owner", "writer", "proposal", "validation"}.issubset(set(sync.get("schema", []))), "sync_schema")
    check("Field State" in sync.get("runtime_does_not_own", []), "sync_no_field_write")
    check("Decision" not in sync.get("runtime_owns", []), "sync_no_decision_owner")
    check(sync.get("rules", {}).get("owner_validation_required") is True, "sync_owner_validation")

    check({"timestamp", "runtime_state", "active_modules", "pending_events", "trace_id"}.issubset(set(snapshot.get("schema", []))), "snapshot_schema")
    check("Temporary Workspace" in snapshot.get("forbidden_persistence", []), "snapshot_no_workspace")
    check("Unverified State" in snapshot.get("forbidden_persistence", []), "snapshot_no_unverified")
    check(snapshot.get("rules", {}).get("snapshot_before_recovery") is True, "snapshot_recovery_rule")

    check({"Wake-up", "Event", "Runtime Context", "Flow Execution Candidate", "State Proposal", "Decision Boundary", "Trace"}.issubset(set(trace.get("chain", []))), "trace_chain")
    check({"trace_id", "wake_id", "event_id", "runtime_context", "flow_reference", "state_proposal_reference"}.issubset(set(trace.get("required_fields", []))), "trace_schema")
    check(trace.get("rules", {}).get("provenance_required") is True, "trace_provenance")
    check(trace.get("rules", {}).get("trace_not_authority") is True, "trace_no_authority")

    check(recovery.get("pipeline") == ["Detect", "Diagnose", "Degrade", "Recover", "Resume"], "recovery_pipeline")
    check({"Module Failure", "Timeout", "State Sync Failure", "Flow Interrupted"}.issubset(set(recovery.get("failure_types", []))), "recovery_types")
    check({"failure_id", "failure_type", "source", "impact", "fallback_candidate", "resume_point", "trace_id"}.issubset(set(recovery.get("schema", []))), "recovery_schema")
    check(recovery.get("rules", {}).get("constitution_immutable") is True, "recovery_constitution_guard")
    check(recovery.get("rules", {}).get("value_immutable") is True, "recovery_value_guard")

    check(set(persistence.get("allowed", [])) == {"Long-term Memory Reference", "Experience Reference", "Important Snapshot"}, "persistence_allowlist")
    check({"Temporary Workspace", "Runtime Cache", "Unverified State"}.issubset(set(persistence.get("forbidden", []))), "persistence_blocklist")
    check(persistence.get("rules", {}).get("unverified_not_persisted") is True, "persistence_unverified_guard")
    check(persistence.get("rules", {}).get("persistence_not_decision") is True, "persistence_no_decision")

    check({"Lifecycle Contract", "Event Contract", "State Contract", "Trace Contract"}.issubset(set(os_interface.get("uses", []))), "os_interface_contracts")
    check("Decision Authority" in os_interface.get("runtime_does_not_modify", []), "os_interface_no_decision")
    check(os_interface.get("rules", {}).get("interface_only") is True, "os_interface_only")
    check({"Attention Refresh Candidate", "Workspace Update Candidate", "Brain Input Package Request"}.issubset(set(core_interface.get("allowed_requests", []))), "core_interface_requests")
    check({"Decision", "Goal", "Value", "Reality"}.issubset(set(core_interface.get("runtime_does_not_own", []))), "core_interface_no_ownership")
    check(core_interface.get("rules", {}).get("candidate_interface_only") is True, "core_interface_candidate_only")

    forbidden = set(boundary.get("forbidden", []))
    for item in ("Runtime → Decision Ownership", "Runtime → Reality Modification", "Runtime → Action Execution", "Capability → Runtime Control", "Emotion → Runtime Scheduling"):
        check(item in forbidden, f"boundary_guard:{item}")
    check(len(boundary.get("allowed", [])) >= 4, "boundary_allowed_edges")
    check(boundary.get("rules", {}).get("no_real_runtime") is True, "boundary_no_runtime")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch", "asyncio"}), "planning_no_runtime_import")
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
    print("READINESS: LUNA_COGNITIVE_RUNTIME_FOUNDATION_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
