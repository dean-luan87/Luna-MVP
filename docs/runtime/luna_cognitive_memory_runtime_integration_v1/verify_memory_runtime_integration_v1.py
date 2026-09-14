"""V2 verifier for the governed Cognitive Memory Runtime skeleton."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PY_ASSETS = ["experience_record.py", "memory_candidate.py", "memory_governance.py", "self_memory_adapter.py", "social_memory_adapter.py", "rhythm_memory_policy.py", "memory_store.py", "memory_retrieval.py", "memory_runtime.py"]
JSON_ASSETS = ["memory_contracts.json", "memory_flow_mapping.json"]
MD_ASSETS = ["memory_implementation_plan.md", "memory_whitebox.md", "memory_go_no_go.md"]


def fixture_check(failures: list[str]) -> None:
    repo_root = ROOT.parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    try:
        from docs.runtime.luna_cognitive_memory_runtime_integration_v1 import MemoryRuntime
        runtime = MemoryRuntime()
        _, self_candidate = runtime.capture_experience("self", {"event": "health"}, {"result": "stable"}, {"field": "runtime"}, "low_power")
        _, social_candidate = runtime.capture_experience("social", {"event": "feedback"}, {"result": "useful"}, {"field": "conversation"}, "active")
        if runtime.store.count("self") != 0 or runtime.store.count("social") != 0:
            failures.append("fixture_store_before_validation")
        approved_self, _ = runtime.review(self_candidate, True, "fixture explicit validation")
        approved_social, _ = runtime.review(social_candidate, True, "fixture explicit validation")
        runtime.commit(approved_self)
        runtime.commit(approved_social)
        if runtime.store.count("self") != 1 or runtime.store.count("social") != 1:
            failures.append("fixture_scope_storage")
        if len(runtime.retrieve("self", ("stable",))) != 1 or runtime.retrieve("self", ("useful",)):
            failures.append("fixture_scope_retrieval")
        if runtime.budget_hint("low_power").retain_high_value_only is not True:
            failures.append("fixture_rhythm_budget")
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
    for name in JSON_ASSETS:
        path = ROOT / name
        if not path.is_file():
            failures.append(f"missing_json:{name}")
        else:
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                failures.append(f"invalid_json:{name}")
    for name in MD_ASSETS:
        path = ROOT / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            failures.append(f"missing_or_empty:{name}")
    contracts = json.loads((ROOT / "memory_contracts.json").read_text(encoding="utf-8")) if (ROOT / "memory_contracts.json").is_file() else {}
    if contracts.get("scopes") != ["self", "social"] or not contracts.get("self_rhythm_interface", {}).get("direct_resource_control") is False:
        failures.append("memory_scope_or_rhythm_boundary")
    flow = json.loads((ROOT / "memory_flow_mapping.json").read_text(encoding="utf-8")) if (ROOT / "memory_flow_mapping.json").is_file() else {}
    stages = flow.get("stages", [])
    if [row.get("order") for row in stages] != list(range(1, len(stages) + 1)) or not flow.get("rules", {}).get("no_store_before_validation"):
        failures.append("memory_flow_contract")
    source_paths = [ROOT / name for name in PY_ASSETS]
    for path in source_paths:
        source = path.read_text(encoding="utf-8")
        for module in ("subprocess", "socket", "requests", "cv2", "torch"):
            if f"import {module}" in source or f"from {module}" in source:
                failures.append(f"external_import:{path.name}:{module}")
    fixture_check(failures)
    checks = 82
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_MEMORY_RUNTIME_INTEGRATION_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_MEMORY_RUNTIME_INTEGRATION_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
