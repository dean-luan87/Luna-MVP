"""Static verifier for the B1 real visual evidence Context/World boundary."""

from __future__ import annotations

import ast
import json
from pathlib import Path


VERIFY_PATH = Path(__file__).resolve()
DOC_DIR = VERIFY_PATH.parent


def _repo_root() -> Path:
    for candidate in (VERIFY_PATH, *VERIFY_PATH.parents):
        if (candidate / "capabilities").is_dir() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("repository root sentinel not found")


ROOT = _repo_root()
GATEWAY_DIR = ROOT / "capabilities/midplatform/core/observation_gateway/integration"
B1_DIR = ROOT / "capabilities/midplatform/core/context_foundation/integration/b1_real_visual_evidence_context_world_controlled"
ARTIFACT_DIR = ROOT / "_eval_out/brain_b1_real_visual_evidence_context_current_world_controlled_implementation_v1"

EXPECTED_GATEWAY_FILES = {
    "__init__.py",
    "real_visual_evidence_gateway_adapter_v1.py",
}
EXPECTED_B1_FILES = {
    "__init__.py",
    "b1_real_visual_evidence_context_world_fixture_v1.py",
    "run_b1_real_visual_evidence_context_world_controlled_implementation_v1.py",
}
EXPECTED_DOC_FILES = {
    "overview_v1.md",
    "implementation_mapping_v1.json",
    "real_evidence_admission_contract_v1.json",
    "context_world_integration_contract_v1.json",
    "field_reducer_boundary_v1.json",
    "trace_provenance_contract_v1.json",
    "differential_validation_v1.json",
    "negative_guards_v1.json",
    "scenario_mapping_v1.json",
    "change_manifest_v1.json",
    "implementation_summary_v1.md",
    "phase_contract.json",
    "verify_b1_real_visual_evidence_context_current_world_controlled_implementation_v1.py",
}


def _regular_source_names(directory: Path) -> set[str]:
    return {item.name for item in directory.iterdir() if item.is_file() and item.suffix == ".py"}


def _check(name: str, condition: bool, detail: str = "") -> dict:
    return {"check": name, "passed": bool(condition), "detail": detail}


def _ast_checks() -> list[dict]:
    checks = []
    files = [
        GATEWAY_DIR / "real_visual_evidence_gateway_adapter_v1.py",
        B1_DIR / "run_b1_real_visual_evidence_context_world_controlled_implementation_v1.py",
    ]
    forbidden = (
        "ultralytics",
        "torch.hub",
        "subprocess",
        "requests",
        "urllib",
        "FieldStateReducer(",
    )
    for path in files:
        exists = path.is_file()
        checks.append(_check(f"implementation exists: {path.name}", exists))
        if not exists:
            continue
        source = path.read_text(encoding="utf-8")
        try:
            ast.parse(source, filename=str(path))
            parsed = True
        except SyntaxError:
            parsed = False
        checks.append(_check(f"AST parses: {path.name}", parsed))
        checks.append(
            _check(
                f"no forbidden provider/runtime path: {path.name}",
                not any(token in source for token in forbidden),
            )
        )
    return checks


def _json_checks() -> list[dict]:
    checks = []
    for path in sorted(DOC_DIR.glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            parsed = True
        except (OSError, json.JSONDecodeError):
            parsed = False
        checks.append(_check(f"JSON parses: {path.name}", parsed))
    return checks


def build_verification() -> dict:
    checks = []
    actual_gateway = _regular_source_names(GATEWAY_DIR)
    actual_b1 = _regular_source_names(B1_DIR)
    actual_docs = {item.name for item in DOC_DIR.iterdir() if item.is_file()}
    checks.extend(
        [
            _check("exact gateway implementation file set", actual_gateway == EXPECTED_GATEWAY_FILES, f"missing={sorted(EXPECTED_GATEWAY_FILES - actual_gateway)} extra={sorted(actual_gateway - EXPECTED_GATEWAY_FILES)}"),
            _check("exact B1 implementation file set", actual_b1 == EXPECTED_B1_FILES, f"missing={sorted(EXPECTED_B1_FILES - actual_b1)} extra={sorted(actual_b1 - EXPECTED_B1_FILES)}"),
            _check("exact documentation file set", actual_docs == EXPECTED_DOC_FILES, f"missing={sorted(EXPECTED_DOC_FILES - actual_docs)} extra={sorted(actual_docs - EXPECTED_DOC_FILES)}"),
        ]
    )
    checks.extend(_ast_checks())
    checks.extend(_json_checks())

    mapping = json.loads((DOC_DIR / "implementation_mapping_v1.json").read_text(encoding="utf-8"))
    guards = json.loads((DOC_DIR / "negative_guards_v1.json").read_text(encoding="utf-8"))
    phase = json.loads((DOC_DIR / "phase_contract.json").read_text(encoding="utf-8"))
    scenarios = json.loads((DOC_DIR / "scenario_mapping_v1.json").read_text(encoding="utf-8"))
    checks.extend(
        [
            _check("canonical owners retained", mapping["new_semantic_owner"] is False),
            _check("existing Context engine reused", mapping["existing_engine_reused"] == "ContextWorldStateControlledIntegrationEngineV1"),
            _check("provider invocation absent in B1", mapping["provider_invocation_in_b1"] is False),
            _check("candidate-only phase", phase["candidate_only"] is True),
            _check("provenance does not grant authority", phase["provenance_grants_authority"] is False),
            _check("23 B1 scenarios registered", scenarios["scenario_count"] == 23 and len(scenarios["scenario_ids"]) == 23),
            _check("reducer remains non-executing", guards["field_state_reducer_is_single_mutation_authority"] is True),
        ]
    )

    summary_path = ARTIFACT_DIR / "b1_real_visual_evidence_context_world_result_v1.json"
    artifact_present = summary_path.is_file()
    checks.append(_check("B1 runner artifact exists", artifact_present))
    if artifact_present:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        checks.extend(
            [
                _check("B1 scenarios pass", summary.get("b1_scenario_count") == 23 and summary.get("all_cases_passed") is True),
                _check("synthetic regression preserved", summary.get("synthetic_regression_preserved") is True),
                _check("Gateway admission reported", summary.get("gateway_admission") is True),
                _check("Context candidate reported", summary.get("context_candidate_created") is True),
                _check("Current World candidate reported", summary.get("current_world_candidate_created") is True),
                _check("Field mutation false", summary.get("field_state_mutation_executed") is False),
                _check("semantic compression false", summary.get("semantic_compression") is False),
            ]
        )
    return {
        "phase": "Phase-Luna-Brain-B1-Real-Visual-Evidence-Context-Current-World-Controlled-Implementation-v1-001",
        "checks": checks,
        "failed_check_count": sum(1 for item in checks if not item["passed"]),
        "blocker_count": sum(1 for item in checks if not item["passed"]),
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


if __name__ == "__main__":
    result = build_verification()
    print(json.dumps(result, indent=2, ensure_ascii=False))
