from __future__ import annotations

import ast
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Set

PHASE_DIR = Path(__file__).resolve().parent


def _resolve_repo_root_from_file() -> Path:
    anchor = Path("capabilities/midplatform/core/context_pcn_intent_mainline")
    for candidate in (PHASE_DIR,) + tuple(PHASE_DIR.parents):
        if (candidate / anchor).is_dir():
            return candidate
    raise RuntimeError(
        "repository root not found from verifier path; expected "
        "capabilities/midplatform/core/context_pcn_intent_mainline"
    )


try:
    REPO_ROOT = _resolve_repo_root_from_file()
except RuntimeError as exc:
    raise SystemExit(f"BOOTSTRAP_ERROR: {exc}")

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

WORKSPACE_ROOT = REPO_ROOT
CODE_DIR = REPO_ROOT / "capabilities/midplatform/core/context_pcn_intent_mainline"
DOC_DIR = (
    REPO_ROOT
    / "docs/architecture/luna_context_pcn_intent_precognitive_mainline_controlled_integration_v1"
)


def _required_doc_files() -> Set[str]:
    return {
        "context_pcn_intent_controlled_integration_overview_v1.md",
        "context_pcn_intent_controlled_execution_contract_v1.json",
        "context_pcn_intent_negative_guards_v1.json",
        "context_pcn_intent_existing_asset_reuse_mapping_v1.json",
        "context_pcn_intent_gap_registry_v1.json",
        "context_pcn_intent_planning_to_code_mapping_v1.json",
        "context_pcn_intent_controlled_change_manifest_v1.json",
        "context_pcn_intent_integration_summary_v1.md",
        "phase_contract.json",
        "verify_context_pcn_intent_controlled_integration_v1.py",
    }


def _required_code_files() -> Set[str]:
    return {
        "__init__.py",
        "context_pcn_intent_mainline_types_v1.py",
        "context_pcn_intent_mainline_error_types_v1.py",
        "context_pcn_intent_mainline_trace_types_v1.py",
        "context_to_pcn_mapping_v1.py",
        "pcn_to_intent_mapping_v1.py",
        "context_pcn_intent_compatibility_v1.py",
        "context_pcn_intent_idempotency_v1.py",
        "context_pcn_intent_static_validators_v1.py",
        "context_pcn_intent_fixture_v1.py",
        "context_pcn_intent_engine_v1.py",
        "run_context_pcn_intent_controlled_integration_v1.py",
    }


def _load_json(path: Path) -> Dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise TypeError(f"{path.name} must be JSON object")
    return obj


def run_verification() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    doc_actual = {p.name for p in DOC_DIR.iterdir() if p.is_file()}
    doc_expected = _required_doc_files()
    checks.append(
        {
            "check_id": "V01_exact_doc_file_set",
            "passed": doc_actual == doc_expected,
            "detail": f"missing={sorted(doc_expected - doc_actual)} extra={sorted(doc_actual - doc_expected)}",
        }
    )

    code_actual = {p.name for p in CODE_DIR.iterdir() if p.is_file()}
    code_expected = _required_code_files()
    checks.append(
        {
            "check_id": "V02_exact_code_file_set",
            "passed": code_actual == code_expected,
            "detail": f"missing={sorted(code_expected - code_actual)} extra={sorted(code_actual - code_expected)}",
        }
    )

    json_files = [
        "context_pcn_intent_controlled_execution_contract_v1.json",
        "context_pcn_intent_negative_guards_v1.json",
        "context_pcn_intent_existing_asset_reuse_mapping_v1.json",
        "context_pcn_intent_gap_registry_v1.json",
        "context_pcn_intent_planning_to_code_mapping_v1.json",
        "context_pcn_intent_controlled_change_manifest_v1.json",
        "phase_contract.json",
    ]
    parse_errors = []
    docs: Dict[str, Dict[str, Any]] = {}
    for name in json_files:
        try:
            docs[name] = _load_json(DOC_DIR / name)
        except Exception as exc:
            parse_errors.append(f"{name}:{exc}")
    checks.append(
        {
            "check_id": "V03_json_parse",
            "passed": len(parse_errors) == 0,
            "detail": ";".join(parse_errors),
        }
    )

    ast_errors = []
    for path in list(DOC_DIR.glob("*.py")) + list(CODE_DIR.glob("*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except Exception as exc:
            ast_errors.append(f"{path.name}:{exc}")
    checks.append(
        {
            "check_id": "V04_ast_parse",
            "passed": len(ast_errors) == 0,
            "detail": ";".join(ast_errors),
        }
    )

    reuse = docs.get("context_pcn_intent_existing_asset_reuse_mapping_v1.json", {})
    checks.append(
        {
            "check_id": "V05_owner_preservation_declared",
            "passed": len(reuse.get("reused_modules", [])) == 3,
            "detail": f"reused_modules={len(reuse.get('reused_modules', []))}",
        }
    )

    gap = docs.get("context_pcn_intent_gap_registry_v1.json", {})
    sot = tuple(gap.get("source_of_truth", []))
    checks.append(
        {
            "check_id": "V06_context_to_pcn_contract_reuse",
            "passed": "docs/architecture/luna_context_foundation_module_closure_v1/context_to_pcn_handoff_contract_candidate.json"
            in sot,
            "detail": str(sot),
        }
    )
    checks.append(
        {
            "check_id": "V07_pcn_to_intent_contract_reuse",
            "passed": "docs/architecture/luna_personal_cognitive_network_module_closure_v1/pcn_to_intent_handoff_contract_candidate_v1.json"
            in sot,
            "detail": str(sot),
        }
    )

    manifest = docs.get("context_pcn_intent_controlled_change_manifest_v1.json", {})
    checks.append(
        {
            "check_id": "V08_no_existing_module_modification",
            "passed": manifest.get("modified_existing_files", []) == [],
            "detail": str(manifest.get("modified_existing_files", [])),
        }
    )

    summary_cls = gap.get("classification_summary", {})
    checks.append(
        {
            "check_id": "V09_gap_classification_completeness",
            "passed": all(k in summary_cls for k in ("A", "B", "C", "D")),
            "detail": str(summary_cls),
        }
    )

    from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_engine_v1 import (
        ContextPcnIntentMainlineEngineV1,
    )
    from capabilities.midplatform.core.context_pcn_intent_mainline.context_pcn_intent_fixture_v1 import (
        get_context_pcn_intent_fixture_cases_v1,
    )

    engine = ContextPcnIntentMainlineEngineV1()
    records = {
        item.scenario_id: item
        for item in engine.run_all(
            tuple(x.directive for x in get_context_pcn_intent_fixture_cases_v1())
        ).scenario_results
    }

    def rec_ok(case_id: str, expected_stop: str) -> bool:
        return case_id in records and records[case_id].stopped_at == expected_stop

    checks.append(
        {
            "check_id": "V10_happy_path",
            "passed": rec_ok("P01", "INTENT_CANDIDATE_READY"),
            "detail": records.get("P01").stopped_at if "P01" in records else "missing",
        }
    )
    checks.append(
        {
            "check_id": "V11_context_incomplete_stop",
            "passed": rec_ok("P02", "STOP_BEFORE_PCN_CONTEXT_INCOMPLETE"),
            "detail": records.get("P02").stopped_at if "P02" in records else "missing",
        }
    )
    checks.append(
        {
            "check_id": "V12_pcn_incomplete_stop",
            "passed": rec_ok("P06", "STOP_BEFORE_INTENT_PCN_INCOMPLETE"),
            "detail": records.get("P06").stopped_at if "P06" in records else "missing",
        }
    )
    checks.append(
        {
            "check_id": "V13_missing_required_ref_reject",
            "passed": rec_ok("P03", "REJECT_CONTEXT_TO_PCN_REQUIRED_REF")
            and rec_ok("P07", "REJECT_PCN_TO_INTENT_REQUIRED_REF"),
            "detail": f"P03={records.get('P03').stopped_at if 'P03' in records else 'missing'},P07={records.get('P07').stopped_at if 'P07' in records else 'missing'}",
        }
    )
    checks.append(
        {
            "check_id": "V14_version_mismatch_hard_block",
            "passed": rec_ok("P04", "HARD_BLOCK_CONTEXT_TO_PCN_VERSION_MISMATCH")
            and rec_ok("P08", "HARD_BLOCK_PCN_TO_INTENT_VERSION_MISMATCH"),
            "detail": f"P04={records.get('P04').stopped_at if 'P04' in records else 'missing'},P08={records.get('P08').stopped_at if 'P08' in records else 'missing'}",
        }
    )
    checks.append(
        {
            "check_id": "V15_duplicate_context_handoff_guard",
            "passed": rec_ok("P09", "STOP_DUPLICATE_CONTEXT_HANDOFF"),
            "detail": records.get("P09").stopped_at if "P09" in records else "missing",
        }
    )
    checks.append(
        {
            "check_id": "V16_duplicate_pcn_handoff_guard",
            "passed": rec_ok("P10", "STOP_DUPLICATE_PCN_HANDOFF"),
            "detail": records.get("P10").stopped_at if "P10" in records else "missing",
        }
    )

    p11 = records.get("P11")
    p12 = records.get("P12")
    checks.append(
        {
            "check_id": "V17_trace_continuity",
            "passed": p11 is not None
            and bool(
                p11.trace.root_trace_id
                and p11.trace.context_trace_ref
                and p11.trace.pcn_trace_ref
                and p11.trace.intent_trace_ref
            ),
            "detail": asdict(p11.trace) if p11 else "missing",
        }
    )
    checks.append(
        {
            "check_id": "V18_provenance_reverse_lookup",
            "passed": p12 is not None
            and p12.provenance.reverse_locatable is True
            and len(p12.provenance.source_context_refs) >= 1,
            "detail": asdict(p12.provenance) if p12 else "missing",
        }
    )

    p13 = records.get("P13")
    p14 = records.get("P14")
    checks.append(
        {
            "check_id": "V19_context_no_direct_intent_mutation",
            "passed": p13 is not None
            and p13.guard_flags.intent_direct_mutation is False
            and p13.guard_flags.context_bypass_to_intent is False,
            "detail": asdict(p13.guard_flags) if p13 else "missing",
        }
    )
    checks.append(
        {
            "check_id": "V20_pcn_no_intent_ownership",
            "passed": p14 is not None
            and p14.guard_flags.pcn_bypass_intent_governance is False,
            "detail": asdict(p14.guard_flags) if p14 else "missing",
        }
    )

    p01 = records.get("P01")
    checks.append(
        {
            "check_id": "V21_intent_governance_formation_authority",
            "passed": p01 is not None
            and p01.intent_candidate_ref.startswith("intent:"),
            "detail": p01.intent_candidate_ref if p01 else "missing",
        }
    )
    checks.append(
        {
            "check_id": "V22_no_runtime_side_effects",
            "passed": p01 is not None
            and p01.guard_flags.runtime_side_effect is False
            and p01.guard_flags.database_write is False
            and p01.guard_flags.device_control is False,
            "detail": asdict(p01.guard_flags) if p01 else "missing",
        }
    )

    runner_path = CODE_DIR / "run_context_pcn_intent_controlled_integration_v1.py"
    checks.append(
        {
            "check_id": "V23_runner_artifacts",
            "passed": runner_path.exists()
            and "_eval_out/context_pcn_intent_mainline_controlled_integration_v1"
            in runner_path.read_text(encoding="utf-8"),
            "detail": str(runner_path),
        }
    )

    passed = [c for c in checks if c["passed"]]
    failed = [c for c in checks if not c["passed"]]

    return {
        "phase_id": "Phase-Luna-Context-PCN-Intent-PreCognitive-Mainline-Controlled-Integration-v1-001",
        "checks": checks,
        "failed_checks": failed,
        "summary": {
            "total_checks": len(checks),
            "passed_check_count": len(passed),
            "failed_check_count": len(failed),
            "blocker_count": len(
                [x for x in failed if "hard_block" in x.get("detail", "")]
            ),
        },
        "final_decision_candidate": "LUNA_CONTEXT_PCN_INTENT_PRECOGNITIVE_MAINLINE_CONTROLLED_INTEGRATION_READY_FOR_USER_V2_VERIFICATION"
        if not failed
        else "LUNA_CONTEXT_PCN_INTENT_PRECOGNITIVE_MAINLINE_CONTROLLED_INTEGRATION_BLOCKED",
        "current_status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "next": "USER_TERMINAL_RUN_CONTEXT_PCN_INTENT_CONTROLLED_INTEGRATION_VERIFIER_V1",
        "note": "Agent must not declare GO. User terminal V2 verification and ChatGPT V3 audit are required.",
    }


if __name__ == "__main__":
    print(json.dumps(run_verification(), ensure_ascii=True, indent=2))
