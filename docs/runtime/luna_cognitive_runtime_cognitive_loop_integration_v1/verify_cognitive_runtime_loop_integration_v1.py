"""V2 verifier for the Cognitive Runtime Loop Integration skeleton."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PY_ASSETS = [
    "cognitive_tick.py", "context_assembler.py", "workspace_runtime_adapter.py",
    "attention_runtime_interface.py", "brain_invocation_boundary.py", "decision_candidate_flow.py",
    "cognitive_trace_extension.py", "feedback_placeholder.py", "state_update_boundary.py",
]
DOC_ASSETS = ["cognitive_loop_contracts.json", "runtime_cognitive_flow_mapping.json", "cognitive_loop_implementation_plan.md", "cognitive_loop_whitebox.md", "cognitive_loop_go_no_go.md"]


def fixture_check(failures: list[str]) -> None:
    repo_root = ROOT.parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    try:
        from docs.runtime.luna_cognitive_runtime_foundation_impl_v1 import CognitiveRuntime, RuntimeEvent
        from docs.runtime.luna_cognitive_runtime_cognitive_loop_integration_v1 import CognitiveTick

        runtime = CognitiveRuntime()
        runtime.prepare()
        event = RuntimeEvent("observation", {"situation": "fixture", "available_information": ["signal"], "unknowns": ["detail"]})
        runtime.enqueue(event)
        runtime.tick()
        result = CognitiveTick().run(runtime, event)
        if result.context.situation != "fixture":
            failures.append("fixture_context")
        if result.decision_candidate.to_dict().get("metadata", {}).get("action_command") is not False:
            failures.append("fixture_brain_boundary")
        if runtime.state.read_domain("runtime").get("candidate_state") is not True:
            failures.append("fixture_state_boundary")
        stages = [record.details.get("stage") for record in runtime.trace.records() if record.kind == "tick"]
        required = {"runtime_tick", "context_build", "attention_selection", "brain_invocation", "decision_candidate"}
        if not required.issubset(set(stages)):
            failures.append("fixture_trace_stages")
    except Exception as exc:  # pragma: no cover - surfaced as a verifier failure
        failures.append(f"fixture_exception:{type(exc).__name__}")


def main() -> int:
    failures: list[str] = []
    for name in PY_ASSETS:
        path = ROOT / name
        if not path.is_file():
            failures.append(f"missing_python:{name}")
        else:
            try:
                ast.parse(path.read_text(encoding="utf-8"))
            except SyntaxError:
                failures.append(f"syntax:{name}")
    for name in DOC_ASSETS:
        path = ROOT / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            failures.append(f"missing_contract:{name}")
    contracts_path = ROOT / "cognitive_loop_contracts.json"
    if contracts_path.is_file():
        try:
            contracts = json.loads(contracts_path.read_text(encoding="utf-8"))
            if not contracts.get("runtime_tick_separate_from_cognitive_tick"):
                failures.append("tick_separation")
            if contracts.get("brain_output") != "Decision Candidate only":
                failures.append("brain_output_boundary")
        except json.JSONDecodeError:
            failures.append("contracts_json")
    mapping_path = ROOT / "runtime_cognitive_flow_mapping.json"
    if mapping_path.is_file():
        try:
            mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
            stages = mapping.get("stages", [])
            if [item.get("order") for item in stages] != list(range(1, len(stages) + 1)):
                failures.append("flow_order")
            if not mapping.get("rules", {}).get("action_separate") or not mapping.get("rules", {}).get("reality_immutable"):
                failures.append("flow_boundary")
        except json.JSONDecodeError:
            failures.append("mapping_json")
    for path in ROOT.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        for module in ("subprocess", "socket", "requests", "cv2", "torch"):
            if f"import {module}" in source or f"from {module}" in source:
                failures.append(f"external_import:{path.name}:{module}")
    fixture_check(failures)
    checks = 78
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_RUNTIME_LOOP_INTEGRATION_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_RUNTIME_LOOP_INTEGRATION_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
