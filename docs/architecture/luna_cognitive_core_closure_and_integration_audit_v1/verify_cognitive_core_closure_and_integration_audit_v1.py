from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Set

PHASE_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    passed: bool
    detail: str


def _expect(condition: bool, check_id: str, ok: str, fail: str) -> CheckResult:
    return CheckResult(
        check_id=check_id, passed=condition, detail=ok if condition else fail
    )


def _required_files() -> Set[str]:
    return {
        "cognitive_core_closure_audit_plan_v1.md",
        "cognitive_core_source_of_truth_registry_v1.json",
        "cognitive_core_owner_closure_matrix_v1.json",
        "cognitive_core_forward_handoff_closure_matrix_v1.json",
        "cognitive_core_feedback_loop_closure_matrix_v1.json",
        "cognitive_core_semantic_inequality_registry_v1.json",
        "cognitive_core_trace_closure_audit_v1.json",
        "cognitive_core_provenance_closure_audit_v1.json",
        "cognitive_core_version_compatibility_matrix_v1.json",
        "cognitive_core_error_namespace_matrix_v1.json",
        "cognitive_core_memory_learning_boundary_audit_v1.json",
        "cognitive_core_freeze_registry_v1.json",
        "cognitive_core_deferred_registry_v1.json",
        "cognitive_core_gap_closure_registry_v1.json",
        "cognitive_core_closure_scenario_audit_v1.json",
        "cognitive_core_readiness_decision_v1.json",
        "cognitive_core_closure_summary_v1.md",
        "cognitive_core_closure_change_manifest_v1.json",
        "phase_contract.json",
        "verify_cognitive_core_closure_and_integration_audit_v1.py",
    }


def _json_files() -> List[str]:
    return sorted([name for name in _required_files() if name.endswith(".json")])


def _load_json(name: str) -> Dict[str, Any]:
    value = json.loads((PHASE_DIR / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{name} must contain a JSON object")
    return value


def run_verification() -> Dict[str, Any]:
    results: List[CheckResult] = []
    actual = {path.name for path in PHASE_DIR.iterdir() if path.is_file()}
    required = _required_files()
    results.append(
        _expect(
            actual == required,
            "A01_exact_required_file_set",
            "Exact required file set present.",
            f"Mismatch. missing={sorted(required - actual)} extra={sorted(actual - required)}",
        )
    )

    docs: Dict[str, Dict[str, Any]] = {}
    parse_failures: List[str] = []
    for name in _json_files():
        try:
            docs[name] = _load_json(name)
        except Exception as exc:
            parse_failures.append(f"{name}:{exc}")
            docs[name] = {}
    results.append(
        _expect(
            not parse_failures,
            "A02_json_parse",
            "All JSON audit assets parse.",
            f"JSON parse failures: {parse_failures}",
        )
    )

    ast_failures: List[str] = []
    try:
        ast.parse(
            (
                PHASE_DIR / "verify_cognitive_core_closure_and_integration_audit_v1.py"
            ).read_text(encoding="utf-8")
        )
    except Exception as exc:
        ast_failures.append(str(exc))
    results.append(
        _expect(
            not ast_failures,
            "A03_ast_parse",
            "Verifier AST parse passed.",
            f"AST parse failures: {ast_failures}",
        )
    )

    phase_contract = docs.get("phase_contract.json", {})
    flags = phase_contract.get("boundary_flags", {})
    expected_false_flags = [
        "runtime_execution",
        "database_write",
        "vector_store_write",
        "embedding_execution",
        "model_call",
        "scheduler_execution",
        "task_mutation",
        "device_control",
        "source_owner_mutation",
        "parameter_activation",
        "genome_activation",
        "memory_persistence",
        "learning_execution",
        "semantic_compression_execution",
        "self_mutation",
        "personality_mutation",
        "emotion_mutation",
        "real_side_effect",
    ]
    results.append(
        _expect(
            phase_contract.get("Execution Mode") == "Audit"
            and flags.get("audit_only") is True
            and flags.get("planning_only") is True
            and all(flags.get(name) is False for name in expected_false_flags),
            "A04_phase_contract_boundary_flags",
            "Phase contract boundary flags match audit-only rules.",
            f"Phase contract mismatch: execution_mode={phase_contract.get('Execution Mode')} flags={flags}",
        )
    )

    owner = docs.get("cognitive_core_owner_closure_matrix_v1.json", {})
    owner_modules = owner.get("modules", [])
    results.append(
        _expect(
            len(owner_modules) == 8
            and owner.get("overall_status") == "CLOSED"
            and owner.get("unresolved_c_blockers") == 0
            and owner.get("audit_assertions", {}).get(
                "flow_lifecycle_only_authority_preserved"
            )
            is True,
            "A05_owner_closure",
            "Owner closure is complete across eight core modules.",
            f"Owner closure mismatch: module_count={len(owner_modules)} data={owner.get('audit_assertions')}",
        )
    )

    handoffs = docs.get(
        "cognitive_core_forward_handoff_closure_matrix_v1.json", {}
    ).get("handoffs", [])
    handoff_ids = {
        item.get("handoff_id") for item in handoffs if isinstance(item, dict)
    }
    blocked_handoffs = [
        item.get("handoff_id")
        for item in handoffs
        if item.get("closure_status") == "BLOCKED"
    ]
    results.append(
        _expect(
            handoff_ids == {"H01", "H02", "H03", "H04", "H05", "H06", "H07"}
            and not blocked_handoffs,
            "A06_forward_handoff_coverage",
            "Forward handoff closure covers H01-H07 with no blocked handoff.",
            f"Forward handoff mismatch: ids={sorted(handoff_ids)} blocked={blocked_handoffs}",
        )
    )

    feedback = docs.get("cognitive_core_feedback_loop_closure_matrix_v1.json", {})
    feedback_paths = feedback.get("feedback_paths", [])
    freeze_assertions = feedback.get("freeze_assertions", {})
    results.append(
        _expect(
            {item.get("feedback_id") for item in feedback_paths}
            == {"F01", "F02", "F03", "F04", "F05"}
            and feedback.get("automatic_self_reinforcing_loop_detected") is False
            and all(bool(value) for value in freeze_assertions.values()),
            "A07_feedback_loop_closure",
            "Feedback loop closure and non-activation guards are present.",
            f"Feedback loop mismatch: freeze_assertions={freeze_assertions}",
        )
    )

    semantic = docs.get("cognitive_core_semantic_inequality_registry_v1.json", {})
    results.append(
        _expect(
            semantic.get("overall_status") == "VERIFIED"
            and len(semantic.get("assertions", [])) >= 15
            and all(
                item.get("status") is True for item in semantic.get("assertions", [])
            ),
            "A08_semantic_inequality_freeze",
            "Semantic inequality registry is complete.",
            f"Semantic inequality mismatch: {semantic.get('assertions')}",
        )
    )

    trace = docs.get("cognitive_core_trace_closure_audit_v1.json", {})
    provenance = docs.get("cognitive_core_provenance_closure_audit_v1.json", {})
    results.append(
        _expect(
            trace.get("root_trace_linkage") is True
            and trace.get("cycle_reverse_locatable") is True
            and all(
                bool(value)
                for value in provenance.get("reverse_locatability", {}).values()
            )
            and provenance.get("rules", {}).get(
                "provenance_continuity_not_fact_authority"
            )
            is True,
            "A09_trace_and_provenance_closure",
            "Trace and provenance closure are reverse-locatable.",
            f"Trace/provenance mismatch: trace={trace} provenance={provenance}",
        )
    )

    versions = docs.get("cognitive_core_version_compatibility_matrix_v1.json", {})
    results.append(
        _expect(
            versions.get("migration_required_count") == 0
            and versions.get("incompatible_count") == 0
            and versions.get("rules", {}).get("no_silent_coercion") is True,
            "A10_version_compatibility",
            "Version compatibility remains within compatible or compatible_with_adapter.",
            f"Version compatibility mismatch: {versions}",
        )
    )

    err = docs.get("cognitive_core_error_namespace_matrix_v1.json", {})
    boundary = docs.get("cognitive_core_memory_learning_boundary_audit_v1.json", {})
    results.append(
        _expect(
            len(err.get("entries", [])) >= 7
            and err.get("rules", {}).get("error_propagation_not_retry_authority")
            is True
            and boundary.get("overall_status") == "CLOSED"
            and boundary.get("semantic_compression", {}).get("status")
            == "DEFERRED_TO_EMOTION_ENGINE",
            "A11_error_namespace_and_memory_learning_boundary",
            "Error namespace matrix and memory/learning boundary audit are complete.",
            f"Boundary mismatch: error_entries={len(err.get('entries', []))} boundary={boundary}",
        )
    )

    freeze = docs.get("cognitive_core_freeze_registry_v1.json", {})
    deferred = docs.get("cognitive_core_deferred_registry_v1.json", {})
    gaps = docs.get("cognitive_core_gap_closure_registry_v1.json", {})
    scenarios = docs.get("cognitive_core_closure_scenario_audit_v1.json", {})
    readiness = docs.get("cognitive_core_readiness_decision_v1.json", {})
    results.append(
        _expect(
            len(freeze.get("freeze_items", [])) >= 14
            and len(deferred.get("deferred_items", [])) >= 16
            and gaps.get("counts", {}).get("C") == 0
            and scenarios.get("scenario_count") == 32
            and readiness.get("decision") == "READY_FOR_SELF_PERSONALITY_EMOTION",
            "A12_freeze_deferred_scenarios_and_readiness",
            "Freeze registry, deferred registry, scenario audit, and readiness decision are coherent.",
            f"Coherence mismatch: freeze={len(freeze.get('freeze_items', []))} deferred={len(deferred.get('deferred_items', []))} gaps={gaps.get('counts')} scenarios={scenarios.get('scenario_count')} readiness={readiness.get('decision')}",
        )
    )

    failed = [item.check_id for item in results if not item.passed]
    checks = {item.check_id: ("pass" if item.passed else "fail") for item in results}
    all_passed = not failed
    return {
        "CHECKS": checks,
        "FAILED_CHECKS": failed,
        "PASSED_CHECK_COUNT": sum(1 for item in results if item.passed),
        "FAILED_CHECK_COUNT": sum(1 for item in results if not item.passed),
        "BLOCKER_COUNT": sum(1 for item in results if not item.passed),
        "FINAL_DECISION": "PASS" if all_passed else "BLOCKED",
        "NEXT": readiness.get("decision", "REMEDIATION_REQUIRED")
        if all_passed
        else "LUNA_COGNITIVE_CORE_CLOSURE_AND_INTEGRATION_AUDIT_REMEDIATION",
        "DETAILS": [
            {"check_id": item.check_id, "detail": item.detail} for item in results
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_verification(), indent=2, ensure_ascii=False))
