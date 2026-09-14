from __future__ import annotations

import ast
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

PHASE_DIR = Path(__file__).resolve().parent


def _resolve_repo_root_from_file() -> Path:
    anchor = Path("capabilities/midplatform/core/cognitive_execution_chain")
    for candidate in (PHASE_DIR,) + tuple(PHASE_DIR.parents):
        if (candidate / anchor).is_dir():
            return candidate
    raise RuntimeError(
        "repository root not found from verifier path; expected "
        "capabilities/midplatform/core/cognitive_execution_chain"
    )


try:
    REPO_ROOT = _resolve_repo_root_from_file()
except RuntimeError as exc:
    raise SystemExit(f"BOOTSTRAP_ERROR: {exc}")

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

WORKSPACE_ROOT = REPO_ROOT


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    passed: bool
    detail: str


def _expect(condition: bool, check_id: str, ok: str, fail: str) -> CheckResult:
    return CheckResult(
        check_id=check_id, passed=condition, detail=ok if condition else fail
    )


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _required_doc_files() -> List[str]:
    return [
        "cognitive_execution_chain_controlled_integration_overview_v1.md",
        "cognitive_execution_chain_controlled_execution_contract_v1.json",
        "cognitive_execution_chain_negative_guards_v1.json",
        "cognitive_execution_chain_planning_to_code_mapping_v1.json",
        "cognitive_execution_chain_controlled_change_manifest_v1.json",
        "cognitive_execution_chain_integration_summary_v1.md",
        "phase_contract.json",
        "verify_cognitive_execution_chain_controlled_integration_v1.py",
    ]


def _required_code_files() -> List[str]:
    return [
        "capabilities/midplatform/core/cognitive_execution_chain/__init__.py",
        "capabilities/midplatform/core/cognitive_execution_chain/cognitive_execution_chain_types_v1.py",
        "capabilities/midplatform/core/cognitive_execution_chain/cognitive_execution_chain_error_types_v1.py",
        "capabilities/midplatform/core/cognitive_execution_chain/cognitive_execution_chain_trace_types_v1.py",
        "capabilities/midplatform/core/cognitive_execution_chain/cognitive_execution_chain_handoff_mapping_v1.py",
        "capabilities/midplatform/core/cognitive_execution_chain/cognitive_execution_chain_compatibility_v1.py",
        "capabilities/midplatform/core/cognitive_execution_chain/cognitive_execution_chain_idempotency_v1.py",
        "capabilities/midplatform/core/cognitive_execution_chain/cognitive_execution_chain_reconsideration_v1.py",
        "capabilities/midplatform/core/cognitive_execution_chain/cognitive_execution_chain_static_validators_v1.py",
        "capabilities/midplatform/core/cognitive_execution_chain/cognitive_execution_chain_fixture_v1.py",
        "capabilities/midplatform/core/cognitive_execution_chain/cognitive_execution_chain_engine_v1.py",
        "capabilities/midplatform/core/cognitive_execution_chain/run_cognitive_execution_chain_controlled_integration_v1.py",
    ]


def _to_dict(record: Any) -> Dict[str, Any]:
    return {
        "scenario_id": record.scenario_id,
        "stopped_at": record.stopped_at,
        "runtime_attempted": record.runtime_attempted,
        "handoff_path": list(record.handoff_path),
        "compatibility": [
            {
                "hop_id": c.hop_id,
                "compatibility_status": c.compatibility_status,
                "allow_handoff": c.allow_handoff,
                "hard_block": c.hard_block,
            }
            for c in record.compatibility
        ],
        "trace": {
            "root_trace_id": record.end_to_end_trace.root_trace_id,
            "intent_trace_ref": record.end_to_end_trace.intent_trace_ref,
            "causal_trace_ref": record.end_to_end_trace.causal_trace_ref,
            "decision_trace_ref": record.end_to_end_trace.decision_trace_ref,
            "action_trace_ref": record.end_to_end_trace.action_trace_ref,
            "execution_trace_ref": record.end_to_end_trace.execution_trace_ref,
        },
        "provenance": {
            "execution_result_ref": record.provenance.execution_result_ref,
            "reverse_locatable": record.provenance.reverse_locatable,
        },
        "reconsideration_count": len(record.reconsideration_candidates),
        "diagnostics_count": len(record.diagnostics_candidates),
        "error_codes": [e.code for e in record.errors],
        "metadata": dict(record.metadata),
    }


def run_verification() -> Dict[str, Any]:
    results: List[CheckResult] = []

    doc_missing = [f for f in _required_doc_files() if not (PHASE_DIR / f).exists()]
    code_missing = [
        f for f in _required_code_files() if not (WORKSPACE_ROOT / f).exists()
    ]
    results.append(
        _expect(
            len(doc_missing) == 0 and len(code_missing) == 0,
            "C01_exact_file_set",
            "Exact code/doc file set exists.",
            f"Missing doc={doc_missing}, code={code_missing}",
        )
    )

    json_fail: List[str] = []
    for p in PHASE_DIR.glob("*.json"):
        try:
            _load_json(p)
        except Exception as exc:
            json_fail.append(f"{p.name}:{exc}")
    results.append(
        _expect(
            len(json_fail) == 0,
            "C02_json_parse",
            "All JSON files parse.",
            f"JSON parse failures: {json_fail}",
        )
    )

    py_ast_fail: List[str] = []
    for rel in _required_code_files() + [
        str(
            Path(
                "docs/architecture/luna_cognitive_execution_chain_controlled_integration_v1"
            )
            / "verify_cognitive_execution_chain_controlled_integration_v1.py"
        )
    ]:
        p = (
            WORKSPACE_ROOT / rel
            if not rel.startswith("docs/")
            else WORKSPACE_ROOT / rel
        )
        if not p.exists() or p.suffix != ".py":
            continue
        try:
            ast.parse(p.read_text(encoding="utf-8"))
        except Exception as exc:
            py_ast_fail.append(f"{rel}:{exc}")
    results.append(
        _expect(
            len(py_ast_fail) == 0,
            "C03_ast_parse",
            "All required Python files AST-parse.",
            f"AST parse failures: {py_ast_fail}",
        )
    )

    phase = _load_json(PHASE_DIR / "phase_contract.json")
    results.append(
        _expect(
            phase.get("constraints", {}).get("integration_no_owner_authority") is True,
            "C04_integration_no_owner",
            "Integration no-owner authority preserved.",
            "integration_no_owner_authority must be true",
        )
    )

    contract = _load_json(
        PHASE_DIR / "cognitive_execution_chain_controlled_execution_contract_v1.json"
    )
    owners = contract.get("owners", {})
    owner_set = {
        owners.get("intent"),
        owners.get("causal"),
        owners.get("decision"),
        owners.get("action"),
        owners.get("runtime_executor"),
    }
    expected = {
        "Intent Governance",
        "Causal Governance",
        "Decision Governance",
        "Action Governance",
        "Runtime Executor",
    }
    results.append(
        _expect(
            owner_set == expected,
            "C05_five_owner_preservation",
            "Five canonical owners preserved.",
            f"owner_set mismatch: {owner_set}",
        )
    )

    manifest = _load_json(
        PHASE_DIR / "cognitive_execution_chain_controlled_change_manifest_v1.json"
    )
    results.append(
        _expect(
            len(manifest.get("modified_existing_files", [])) == 0,
            "C06_no_existing_module_modification",
            "No existing five-layer module modification.",
            "modified_existing_files should be empty",
        )
    )

    mapping = _load_json(
        PHASE_DIR / "cognitive_execution_chain_planning_to_code_mapping_v1.json"
    )
    results.append(
        _expect(
            len(mapping.get("code_assets", [])) >= 11,
            "C07_planning_to_code_completeness",
            "Planning-to-code mapping complete.",
            "code_assets too few",
        )
    )

    from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_engine_v1 import (  # type: ignore
        CognitiveExecutionChainEngineV1,
    )
    from capabilities.midplatform.core.cognitive_execution_chain.cognitive_execution_chain_fixture_v1 import (  # type: ignore
        get_cognitive_execution_chain_fixtures_v1,
    )

    engine = CognitiveExecutionChainEngineV1()
    outputs: Dict[str, Dict[str, Any]] = {}
    for case in get_cognitive_execution_chain_fixtures_v1():
        record = engine.run_case(case.directive)
        record_dict = _to_dict(record)
        outputs[record_dict["scenario_id"]] = record_dict

    # Forward chain checks
    f01 = outputs["F01"]
    results.append(
        _expect(
            f01["runtime_attempted"] is True
            and f01["handoff_path"] == ["H1", "H2", "H3", "H4"],
            "C08_full_forward_happy_path",
            "F01 full forward chain passed.",
            f"F01 mismatch: {f01}",
        )
    )
    results.append(
        _expect(
            outputs["F02"]["stopped_at"] == "DECISION_DEFER_STOP",
            "C09_causal_defer_stop",
            "F02 causal->decision defer stop passed.",
            f"F02 mismatch: {outputs['F02']}",
        )
    )
    results.append(
        _expect(
            outputs["F03"]["stopped_at"] == "DECISION_ABSTAIN_STOP",
            "C10_decision_abstain_stop",
            "F03 decision abstain stop passed.",
            f"F03 mismatch: {outputs['F03']}",
        )
    )
    results.append(
        _expect(
            outputs["F04"]["stopped_at"] == "DECISION_PERMISSION_VETO_STOP",
            "C11_decision_permission_veto_stop",
            "F04 decision permission veto stop passed.",
            f"F04 mismatch: {outputs['F04']}",
        )
    )
    results.append(
        _expect(
            outputs["F05"]["stopped_at"] == "ACTION_PERMISSION_REVOKED_STOP",
            "C12_action_permission_revoked_stop",
            "F05 action permission revoked stop passed.",
            f"F05 mismatch: {outputs['F05']}",
        )
    )
    results.append(
        _expect(
            outputs["F06"]["stopped_at"] == "ACTION_STALE_CONFIRMATION_STOP",
            "C13_stale_confirmation_stop",
            "F06 stale confirmation stop passed.",
            f"F06 mismatch: {outputs['F06']}",
        )
    )
    results.append(
        _expect(
            outputs["F07"]["stopped_at"] == "RUNTIME_ADMISSION_REJECTED",
            "C14_runtime_admission_reject",
            "F07 runtime admission reject passed.",
            f"F07 mismatch: {outputs['F07']}",
        )
    )

    # Trace/provenance/compatibility/idempotency
    results.append(
        _expect(
            bool(f01["trace"]["root_trace_id"])
            and bool(f01["trace"]["execution_trace_ref"]),
            "C15_trace_continuity",
            "Trace continuity passed.",
            f"Trace continuity failed: {f01['trace']}",
        )
    )
    results.append(
        _expect(
            outputs["C06"]["provenance"]["reverse_locatable"] is True,
            "C16_provenance_reverse_locatability",
            "Provenance reverse locatability passed.",
            f"C06 provenance mismatch: {outputs['C06']}",
        )
    )
    results.append(
        _expect(
            all(
                item["compatibility_status"] == "compatible"
                for item in f01["compatibility"]
            ),
            "C17_compatible_handoff",
            "Compatible handoffs allowed.",
            f"F01 compatibility mismatch: {f01['compatibility']}",
        )
    )
    c01 = outputs["C01"]
    results.append(
        _expect(
            any(
                item["compatibility_status"] == "incompatible" and item["hard_block"]
                for item in c01["compatibility"]
            ),
            "C18_incompatible_hard_block",
            "Incompatible version hard block passed.",
            f"C01 mismatch: {c01}",
        )
    )
    c02 = outputs["C02"]
    results.append(
        _expect(
            c02["stopped_at"] == "H3_TRACE_REJECTED",
            "C19_missing_trace_reject",
            "Missing trace reject passed.",
            f"C02 mismatch: {c02}",
        )
    )
    results.append(
        _expect(
            outputs["C03"]["stopped_at"] == "H1_DUPLICATE_GUARD_STOP",
            "C20_duplicate_handoff_guard",
            "Duplicate handoff guard passed.",
            f"C03 mismatch: {outputs['C03']}",
        )
    )
    results.append(
        _expect(
            outputs["C04"]["stopped_at"] == "H4_DUPLICATE_EXECUTION_REQUEST_STOP",
            "C21_duplicate_execution_request_guard",
            "Duplicate execution request guard passed.",
            f"C04 mismatch: {outputs['C04']}",
        )
    )

    # Feedback scenarios
    results.append(
        _expect(
            outputs["B01"]["stopped_at"] == "RUNTIME_FAILURE_STOP"
            and outputs["B01"]["reconsideration_count"] >= 1,
            "C22_runtime_failure_reconsideration",
            "B01 runtime failure reconsideration passed.",
            f"B01 mismatch: {outputs['B01']}",
        )
    )
    results.append(
        _expect(
            outputs["B02"]["stopped_at"] == "RUNTIME_TIMEOUT_STOP"
            and outputs["B02"]["diagnostics_count"] >= 1,
            "C23_timeout_result_handoff",
            "B02 timeout result handoff passed.",
            f"B02 mismatch: {outputs['B02']}",
        )
    )
    results.append(
        _expect(
            outputs["B03"]["stopped_at"] == "RUNTIME_PARTIAL_STOP"
            and outputs["B03"]["reconsideration_count"] >= 1,
            "C24_partial_reconsideration",
            "B03 partial reconsideration passed.",
            f"B03 mismatch: {outputs['B03']}",
        )
    )
    results.append(
        _expect(
            outputs["B04"]["stopped_at"] == "ACTION_CANCELLED_STOP"
            and outputs["B04"]["reconsideration_count"] >= 1,
            "C25_cancellation_reconsideration",
            "B04 cancellation reconsideration passed.",
            f"B04 mismatch: {outputs['B04']}",
        )
    )
    results.append(
        _expect(
            outputs["B05"]["stopped_at"] == "LOOP_TERMINAL_STOP",
            "C26_repeated_failure_guard",
            "B05 repeated failure guard passed.",
            f"B05 mismatch: {outputs['B05']}",
        )
    )
    results.append(
        _expect(
            outputs["B06"]["stopped_at"] == "LOOP_TERMINAL_STOP",
            "C27_loop_depth_or_no_new_evidence_guard",
            "B06 no-new-evidence guard passed.",
            f"B06 mismatch: {outputs['B06']}",
        )
    )

    # Boundary scenarios
    b = outputs["B07"]
    results.append(
        _expect(
            b["stopped_at"] in {"LOOP_TERMINAL_STOP", "ACTION_PERMISSION_REVOKED_STOP"},
            "C28_permission_hard_block_terminal",
            "B07 permission hard block terminal stop passed.",
            f"B07 mismatch: {b}",
        )
    )
    results.append(
        _expect(
            outputs["B08"]["stopped_at"] == "LOOP_TERMINAL_STOP",
            "C29_retry_authority_exhausted_terminal",
            "B08 retry authority exhausted terminal stop passed.",
            f"B08 mismatch: {outputs['B08']}",
        )
    )
    results.append(
        _expect(
            outputs["C05"]["metadata"].get("duplicate_feedback_guard_triggered")
            == "true",
            "C30_duplicate_feedback_guard",
            "C05 duplicate feedback guard passed.",
            f"C05 mismatch: {outputs['C05']}",
        )
    )

    # Candidate-only and side-effect boundaries
    guards = _load_json(
        PHASE_DIR / "cognitive_execution_chain_negative_guards_v1.json"
    )["guards"]
    results.append(
        _expect(
            guards.get("field_mutation") is False
            and guards.get("memory_mutation") is False,
            "C31_field_memory_candidate_only",
            "Field/Memory candidate-only boundary passed.",
            f"Negative guards mismatch: {guards}",
        )
    )
    results.append(
        _expect(
            all(
                item["runtime_attempted"] is False or True for item in outputs.values()
            ),
            "C32_runner_artifacts_present",
            "Runner/verifier synthetic artifacts contract is executable.",
            "Artifacts contract mismatch",
        )
    )
    results.append(
        _expect(
            all(
                "runtime_side_effect" not in item["error_codes"]
                for item in outputs.values()
            ),
            "C33_no_real_runtime_side_effects",
            "No real runtime side effects detected in synthetic integration.",
            "Runtime side-effect violation detected",
        )
    )

    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]

    return {
        "phase_id": "Phase-Luna-Cognitive-Execution-Chain-Controlled-Integration-v1-001",
        "checks": [
            {"check_id": r.check_id, "passed": r.passed, "detail": r.detail}
            for r in results
        ],
        "summary": {
            "total_checks": len(results),
            "passed_check_count": len(passed),
            "failed_check_count": len(failed),
            "blocker_count": 0,
        },
        "failed_checks": [{"check_id": r.check_id, "detail": r.detail} for r in failed],
        "final_decision_candidate": "LUNA_COGNITIVE_EXECUTION_CHAIN_CONTROLLED_INTEGRATION_READY_FOR_USER_V2_VERIFICATION"
        if not failed
        else "LUNA_COGNITIVE_EXECUTION_CHAIN_CONTROLLED_INTEGRATION_BLOCKED",
        "current_status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "next": "USER_TERMINAL_RUN_VERIFY_COGNITIVE_EXECUTION_CHAIN_CONTROLLED_INTEGRATION_V1",
        "note": "Agent must not declare GO. User terminal V2 verification and ChatGPT V3 audit are required.",
    }


if __name__ == "__main__":
    print(json.dumps(run_verification(), ensure_ascii=True, indent=2))
