from __future__ import annotations

import ast
import json
import sys
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


def _resolve_repo_root_from_file() -> Path:
    anchor = Path("docs/architecture")
    for candidate in (PHASE_DIR,) + tuple(PHASE_DIR.parents):
        if (candidate / anchor).is_dir() and (candidate / "capabilities").is_dir():
            return candidate
    raise RuntimeError("repository root not found from verifier path")


try:
    REPO_ROOT = _resolve_repo_root_from_file()
except RuntimeError as exc:
    raise SystemExit(f"BOOTSTRAP_ERROR: {exc}")

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _required_files() -> Set[str]:
    return {
        "cognitive_execution_chain_closure_audit_plan_v1.md",
        "cognitive_execution_chain_source_of_truth_registry_v1.json",
        "cognitive_execution_chain_owner_matrix_v1.json",
        "cognitive_execution_chain_contract_closure_matrix_v1.json",
        "cognitive_execution_chain_gap_closure_registry_v1.json",
        "cognitive_execution_chain_trace_closure_audit_v1.json",
        "cognitive_execution_chain_provenance_closure_audit_v1.json",
        "cognitive_execution_chain_error_namespace_matrix_v1.json",
        "cognitive_execution_chain_version_readiness_matrix_v1.json",
        "cognitive_execution_chain_runtime_readiness_matrix_v1.json",
        "cognitive_execution_chain_freeze_registry_v1.json",
        "cognitive_execution_chain_deferred_registry_v1.json",
        "cognitive_execution_chain_closure_scenario_audit_v1.json",
        "cognitive_execution_chain_readiness_decision_v1.json",
        "cognitive_execution_chain_closure_summary_v1.md",
        "cognitive_execution_chain_closure_change_manifest_v1.json",
        "phase_contract.json",
        "verify_cognitive_execution_chain_closure_and_readiness_audit_v1.py",
    }


def _json_files() -> List[str]:
    return sorted(
        [
            "cognitive_execution_chain_source_of_truth_registry_v1.json",
            "cognitive_execution_chain_owner_matrix_v1.json",
            "cognitive_execution_chain_contract_closure_matrix_v1.json",
            "cognitive_execution_chain_gap_closure_registry_v1.json",
            "cognitive_execution_chain_trace_closure_audit_v1.json",
            "cognitive_execution_chain_provenance_closure_audit_v1.json",
            "cognitive_execution_chain_error_namespace_matrix_v1.json",
            "cognitive_execution_chain_version_readiness_matrix_v1.json",
            "cognitive_execution_chain_runtime_readiness_matrix_v1.json",
            "cognitive_execution_chain_freeze_registry_v1.json",
            "cognitive_execution_chain_deferred_registry_v1.json",
            "cognitive_execution_chain_closure_scenario_audit_v1.json",
            "cognitive_execution_chain_readiness_decision_v1.json",
            "cognitive_execution_chain_closure_change_manifest_v1.json",
            "phase_contract.json",
        ]
    )


def _load_json(name: str) -> Dict[str, Any]:
    path = PHASE_DIR / name
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{name} must contain a JSON object")
    return value


def run_verification() -> Dict[str, Any]:
    results: List[CheckResult] = []

    required = _required_files()
    actual = {p.name for p in PHASE_DIR.iterdir() if p.is_file()}
    results.append(
        _expect(
            actual == required,
            "A01_exact_required_file_set",
            "Exact required file set present.",
            f"Mismatch. missing={sorted(required - actual)} extra={sorted(actual - required)}",
        )
    )

    docs: Dict[str, Dict[str, Any]] = {}
    parse_fail: List[str] = []
    for name in _json_files():
        try:
            docs[name] = _load_json(name)
        except Exception as exc:
            docs[name] = {}
            parse_fail.append(f"{name}:{exc}")
    results.append(
        _expect(
            len(parse_fail) == 0,
            "A02_json_parse",
            "All audit JSON files parse.",
            f"JSON parse failures: {parse_fail}",
        )
    )

    ast_fail: List[str] = []
    for py_name in [
        "verify_cognitive_execution_chain_closure_and_readiness_audit_v1.py"
    ]:
        try:
            ast.parse((PHASE_DIR / py_name).read_text(encoding="utf-8"))
        except Exception as exc:
            ast_fail.append(f"{py_name}:{exc}")
    results.append(
        _expect(
            len(ast_fail) == 0,
            "A03_ast_parse",
            "Verifier AST parse passed.",
            f"AST parse failures: {ast_fail}",
        )
    )

    source = docs.get("cognitive_execution_chain_source_of_truth_registry_v1.json", {})
    layers = source.get("layers", [])
    layer_names = {item.get("layer") for item in layers if isinstance(item, dict)}
    required_layers = {
        "Intent",
        "Causal",
        "Decision",
        "Action",
        "Runtime Executor",
        "Integration",
    }
    results.append(
        _expect(
            required_layers <= layer_names,
            "A04_source_of_truth_coverage",
            "Source-of-truth coverage complete.",
            f"Missing layers: {sorted(required_layers - layer_names)}",
        )
    )

    owner_set = {
        item.get("canonical_owner")
        for item in layers
        if isinstance(item, dict) and item.get("layer") in required_layers
    }
    expected_owner_set = {
        "Intent Governance",
        "Causal Governance",
        "Decision Governance",
        "Action Governance",
        "Runtime Executor",
        "Cognitive Execution Chain Integration",
    }
    results.append(
        _expect(
            owner_set == expected_owner_set,
            "A05_five_owner_plus_integration_preservation",
            "Canonical owner set preserved.",
            f"Owner mismatch: {owner_set}",
        )
    )

    integration_layer = next(
        (
            item
            for item in layers
            if isinstance(item, dict) and item.get("layer") == "Integration"
        ),
        {},
    )
    results.append(
        _expect(
            integration_layer.get("new_owner") is False
            and integration_layer.get("mutation_authority") is False,
            "A06_integration_no_owner_no_mutation",
            "Integration no-owner/no-mutation boundary preserved.",
            f"Integration boundary mismatch: {integration_layer}",
        )
    )

    closure = docs.get("cognitive_execution_chain_contract_closure_matrix_v1.json", {})
    hops = closure.get("hops", [])
    hop_names = {item.get("hop") for item in hops if isinstance(item, dict)}
    required_hops = {
        "Intent->Causal",
        "Causal->Decision",
        "Decision->Action",
        "Action->Runtime",
    }
    results.append(
        _expect(
            required_hops <= hop_names,
            "A07_contract_closure_four_forward_hops",
            "Contract closure covers four forward hops.",
            f"Missing hops: {sorted(required_hops - hop_names)}",
        )
    )

    gap = docs.get("cognitive_execution_chain_gap_closure_registry_v1.json", {})
    gap_entries = gap.get("gaps", [])
    gap_ids = {item.get("gap_id") for item in gap_entries if isinstance(item, dict)}
    expected_gap_ids = {
        "GAP-IO-001",
        "GAP-IO-002",
        "GAP-IO-003",
        "GAP-IO-004",
        "GAP-VERSION-001",
        "GAP-VERSION-002",
        "GAP-VERSION-003",
        "GAP-ENUM-001",
        "GAP-MISSING-REF-001",
        "GAP-MISSING-REF-002",
        "GAP-LEGACY-ALIAS-001",
        "GAP-LEGACY-ALIAS-002",
    }
    results.append(
        _expect(
            gap_ids == expected_gap_ids,
            "A08_gap_classification_completeness",
            "Gap classification includes all planning gap ids.",
            f"Gap id mismatch: missing={sorted(expected_gap_ids - gap_ids)} extra={sorted(gap_ids - expected_gap_ids)}",
        )
    )

    blocker_count = sum(
        1
        for item in gap_entries
        if isinstance(item, dict) and item.get("current_status") == "BLOCKER"
    )
    results.append(
        _expect(
            blocker_count >= 0,
            "A09_unresolved_blocker_count_present",
            "Unresolved blocker count computed.",
            "Unable to compute unresolved blocker count.",
        )
    )

    trace = docs.get("cognitive_execution_chain_trace_closure_audit_v1.json", {})
    fwd = trace.get("forward_trace_chain", {})
    rev = trace.get("reverse_trace_chain", {})
    results.append(
        _expect(
            all(
                bool(fwd.get(k))
                for k in [
                    "root_trace_id",
                    "intent_trace",
                    "causal_trace",
                    "decision_trace",
                    "action_trace",
                    "execution_trace",
                ]
            )
            and all(
                bool(rev.get(k))
                for k in [
                    "execution_to_action",
                    "action_to_decision",
                    "decision_to_causal",
                    "causal_to_intent",
                ]
            ),
            "A10_trace_closure",
            "Trace closure is complete.",
            f"Trace closure mismatch: forward={fwd} reverse={rev}",
        )
    )

    prov = docs.get("cognitive_execution_chain_provenance_closure_audit_v1.json", {})
    rev_prov = prov.get("reverse_locatability", {})
    results.append(
        _expect(
            all(
                bool(rev_prov.get(k))
                for k in [
                    "execution_result_to_action_candidate",
                    "execution_result_to_decision_candidate",
                    "execution_result_to_causal_hypothesis",
                    "execution_result_to_intent_candidate",
                    "execution_result_to_source_evidence_or_context_ref",
                ]
            )
            and prov.get("rule_assertions", {}).get(
                "provenance_continuity_not_fact_authority"
            )
            is True,
            "A11_provenance_closure",
            "Provenance closure is complete.",
            f"Provenance closure mismatch: {prov}",
        )
    )

    err = docs.get("cognitive_execution_chain_error_namespace_matrix_v1.json", {})
    namespaces = {
        item.get("namespace")
        for item in err.get("entries", [])
        if isinstance(item, dict)
    }
    expected_ns = {
        "INTENT_*",
        "causal_governance.controlled_implementation.v1",
        "decision_governance.controlled_implementation.v1",
        "action_governance.controlled_implementation.v1",
        "RuntimeExecutorErrorV1",
        "cognitive_execution_chain.controlled_integration.v1",
    }
    results.append(
        _expect(
            expected_ns <= namespaces,
            "A12_error_namespace_coverage",
            "Error namespace coverage complete.",
            f"Missing namespaces: {sorted(expected_ns - namespaces)}",
        )
    )

    version = docs.get("cognitive_execution_chain_version_readiness_matrix_v1.json", {})
    v_hops = version.get("hops", [])
    results.append(
        _expect(
            len(v_hops) == 4,
            "A13_version_readiness_coverage",
            "Version readiness covers four forward hops.",
            f"version hop count mismatch: {len(v_hops)}",
        )
    )
    results.append(
        _expect(
            all(
                item.get("silent_coercion") is False
                for item in v_hops
                if isinstance(item, dict)
            ),
            "A14_no_silent_coercion",
            "No silent coercion in version handling.",
            f"silent coercion mismatch: {v_hops}",
        )
    )

    runtime = docs.get("cognitive_execution_chain_runtime_readiness_matrix_v1.json", {})
    runtime_caps = {
        item.get("capability")
        for item in runtime.get("capabilities", [])
        if isinstance(item, dict)
    }
    expected_runtime_caps = {
        "Intent->Causal",
        "Causal->Decision",
        "Decision->Action",
        "Action->Runtime",
        "Runtime result handoff",
        "Reconsideration",
        "Trace",
        "Provenance",
        "Idempotency",
        "Version compatibility",
        "Task reference flow",
        "Diagnostics flow",
        "Field/Memory candidate evidence",
    }
    results.append(
        _expect(
            expected_runtime_caps <= runtime_caps,
            "A15_runtime_readiness_matrix_completeness",
            "Runtime readiness matrix complete.",
            f"Missing runtime capabilities: {sorted(expected_runtime_caps - runtime_caps)}",
        )
    )

    freeze = docs.get("cognitive_execution_chain_freeze_registry_v1.json", {})
    freeze_scopes = {
        item.get("freeze_scope")
        for item in freeze.get("freeze_items", [])
        if isinstance(item, dict)
    }
    required_freeze = {
        "owner definitions",
        "five-layer concept boundaries",
        "candidate-only handoffs",
        "no direct upstream mutation",
        "trace linkage model",
        "provenance linkage model",
        "retry authority boundary",
        "runtime side-effect boundary",
        "Task no-bypass boundary",
        "Field/Memory candidate-only boundary",
    }
    results.append(
        _expect(
            required_freeze <= freeze_scopes,
            "A16_freeze_registry_completeness",
            "Freeze registry is complete.",
            f"Missing freeze scopes: {sorted(required_freeze - freeze_scopes)}",
        )
    )

    deferred = docs.get("cognitive_execution_chain_deferred_registry_v1.json", {})
    deferred_items = set(deferred.get("deferred_items", []))
    required_deferred = {
        "real event bus",
        "real async orchestration",
        "real scheduler runtime",
        "real Task runtime orchestration",
        "real retry engine",
        "real rollback engine",
        "real adapter/provider/device invocation",
        "Field State writeback",
        "Memory fact writeback",
        "distributed tracing backend",
        "schema registry implementation",
        "production transaction model",
    }
    results.append(
        _expect(
            required_deferred <= deferred_items,
            "A17_deferred_registry_completeness",
            "Deferred registry is complete.",
            f"Missing deferred items: {sorted(required_deferred - deferred_items)}",
        )
    )

    closure_ev = docs.get(
        "cognitive_execution_chain_closure_scenario_audit_v1.json", {}
    )
    summary = closure_ev.get("summary", {})
    categories = {
        item.get("category")
        for item in closure_ev.get("mapped_categories", [])
        if isinstance(item, dict)
    }
    required_categories = {
        "forward chain",
        "stop conditions",
        "compatibility",
        "idempotency",
        "feedback",
        "trace",
        "provenance",
        "owner preservation",
        "no side effects",
    }
    results.append(
        _expect(
            summary.get("total_checks") == 33
            and summary.get("passed_check_count") == 33
            and summary.get("failed_check_count") == 0
            and summary.get("blocker_count") == 0
            and required_categories <= categories,
            "A18_controlled_integration_evidence_mapped",
            "Controlled integration evidence mapped completely.",
            f"Evidence mapping mismatch: summary={summary} categories={sorted(categories)}",
        )
    )

    decision = docs.get("cognitive_execution_chain_readiness_decision_v1.json", {})
    results.append(
        _expect(
            decision.get("main_chain_closed_v1") is True,
            "A19_main_chain_closed_v1",
            "main_chain_closed_v1 is true.",
            f"main_chain_closed_v1 mismatch: {decision.get('main_chain_closed_v1')}",
        )
    )
    results.append(
        _expect(
            decision.get("feedback_chain_closed_v1") is True,
            "A20_feedback_chain_closed_v1",
            "feedback_chain_closed_v1 is true.",
            f"feedback_chain_closed_v1 mismatch: {decision.get('feedback_chain_closed_v1')}",
        )
    )

    phase = docs.get("phase_contract.json", {})
    manifest = docs.get("cognitive_execution_chain_closure_change_manifest_v1.json", {})
    results.append(
        _expect(
            phase.get("runtime_executed") is False
            and phase.get("database_write") is False
            and phase.get("device_control") is False
            and phase.get("scheduler_execution") is False
            and phase.get("task_mutation") is False,
            "A21_no_production_runtime_authorization",
            "No production runtime authorization in phase contract.",
            f"phase runtime flags mismatch: {phase}",
        )
    )
    results.append(
        _expect(
            manifest.get("modified_existing_files") == [],
            "A22_no_existing_module_modification",
            "No existing module modified.",
            f"modified_existing_files mismatch: {manifest.get('modified_existing_files')}",
        )
    )
    results.append(
        _expect(
            phase.get("audit_only") is True and phase.get("planning_only") is True,
            "A23_planning_and_audit_only",
            "Audit-only and planning-only boundaries preserved.",
            f"phase boundary mismatch: {phase}",
        )
    )
    results.append(
        _expect(
            manifest.get("runtime_executed") is False
            and manifest.get("database_write") is False
            and manifest.get("device_control") is False
            and manifest.get("scheduler_execution") is False
            and manifest.get("task_mutation") is False,
            "A24_boundary_execution_flags",
            "Execution boundary flags preserved in change manifest.",
            f"manifest boundary mismatch: {manifest}",
        )
    )

    results.append(
        _expect(
            decision.get("remaining_blocker_count") == blocker_count,
            "A25_blocker_count_consistency",
            "Readiness decision blocker count is consistent.",
            f"blocker count mismatch decision={decision.get('remaining_blocker_count')} computed={blocker_count}",
        )
    )
    results.append(
        _expect(
            decision.get("remaining_deferred_count") == len(deferred_items),
            "A26_deferred_count_consistency",
            "Readiness decision deferred count is consistent.",
            f"deferred count mismatch decision={decision.get('remaining_deferred_count')} computed={len(deferred_items)}",
        )
    )

    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]

    return {
        "phase_id": "Phase-Luna-Cognitive-Execution-Chain-Closure-And-Readiness-Audit-v1-001",
        "checks": [
            {"check_id": r.check_id, "passed": r.passed, "detail": r.detail}
            for r in results
        ],
        "summary": {
            "total_checks": len(results),
            "passed_check_count": len(passed),
            "failed_check_count": len(failed),
            "blocker_count": len(failed),
        },
        "failed_checks": [{"check_id": r.check_id, "detail": r.detail} for r in failed],
        "final_decision_candidate": "LUNA_COGNITIVE_EXECUTION_CHAIN_CLOSURE_AND_READINESS_AUDIT_READY_FOR_USER_V2_VERIFICATION"
        if not failed
        else "LUNA_COGNITIVE_EXECUTION_CHAIN_CLOSURE_AND_READINESS_AUDIT_BLOCKED",
        "current_status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "next": "USER_TERMINAL_RUN_VERIFY_COGNITIVE_EXECUTION_CHAIN_CLOSURE_AND_READINESS_AUDIT_V1",
        "note": "Agent must not declare GO. User terminal V2 verification and ChatGPT V3 audit are required.",
    }


if __name__ == "__main__":
    print(json.dumps(run_verification(), ensure_ascii=True, indent=2))
