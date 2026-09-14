"""User-terminal static verifier for the Personality Governance v1 baseline freeze."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any, Dict, List, Set


def _find_repo_root(start: Path) -> Path:
    """Walk upward to a stable repository sentinel; never depend on cwd."""
    for candidate in (start, *start.parents):
        if (
            (candidate / "capabilities").is_dir()
            and (candidate / "docs").is_dir()
            and (candidate / "README.md").is_file()
        ):
            return candidate
    raise RuntimeError("stable repository sentinel not found")


PHASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = _find_repo_root(PHASE_DIR)
EVAL_DIR = REPO_ROOT / "_eval_out/personality_governance_controlled_implementation_v1"
PLANNING_DIR = REPO_ROOT / "docs/architecture/luna_personality_governance_architecture_planning_v1"
IMPLEMENTATION_DIR = REPO_ROOT / "docs/architecture/luna_personality_governance_controlled_implementation_v1"
CODE_DIR = REPO_ROOT / "capabilities/midplatform/core/personality_governance"

FREEZE_FILES: Set[str] = {
    "personality_governance_baseline_manifest_v1.json",
    "personality_governance_frozen_boundary_registry_v1.json",
    "personality_governance_frozen_deferred_registry_v1.json",
    "personality_governance_baseline_closure_summary_v1.md",
    "phase_contract.json",
    "verify_personality_governance_baseline_freeze_v1.py",
}
EXPECTED_SCENARIOS = {f"P{index:02d}" for index in range(1, 37)}
EXPECTED_DEFERRED = {
    "semantic compression",
    "affective memory compression",
    "emotion memory summary",
    "personality-memory semantic fusion",
    "trait activation",
    "real persistence/runtime",
    "cross-user transfer",
}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_verification() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    actual_freeze = {path.name for path in PHASE_DIR.iterdir() if path.is_file()} if PHASE_DIR.is_dir() else set()
    add(
        "exact_freeze_file_set",
        actual_freeze == FREEZE_FILES,
        f"missing={sorted(FREEZE_FILES - actual_freeze)} extra={sorted(actual_freeze - FREEZE_FILES)}",
    )

    json_names = sorted(name for name in FREEZE_FILES if name.endswith(".json"))
    documents: Dict[str, Any] = {}
    json_failures: List[str] = []
    for name in json_names:
        try:
            documents[name] = _json(PHASE_DIR / name)
        except Exception as exc:
            json_failures.append(f"{name}:{exc}")
            documents[name] = {}
    add("freeze_json_parse", not json_failures, str(json_failures) if json_failures else "freeze JSON parsed")

    source_failures: List[str] = []
    for path in [PHASE_DIR / "verify_personality_governance_baseline_freeze_v1.py"]:
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except Exception as exc:
            source_failures.append(f"{path.name}:{exc}")
    add("freeze_verifier_static_parse", not source_failures, str(source_failures) if source_failures else "freeze verifier source parsed")

    manifest = documents.get("personality_governance_baseline_manifest_v1.json", {})
    add(
        "freeze_status_and_owner",
        manifest.get("freeze_status") == "FROZEN_V1" and manifest.get("canonical_owner") == "Personality Governance",
        "baseline status and canonical owner are frozen",
    )

    boundary = documents.get("personality_governance_frozen_boundary_registry_v1.json", {})
    contract = manifest.get("contract_invariants", {})
    add(
        "contract_semantics_frozen",
        contract.get("personality_trait_not_self") is True
        and contract.get("personality_trait_not_emotion") is True
        and contract.get("personality_trait_not_memory") is True
        and contract.get("personality_candidate_not_personality_truth") is True
        and contract.get("candidate_only") is True
        and contract.get("trait_activation") is False
        and contract.get("fact_admission") is False
        and boundary.get("candidate_boundary", {}).get("activated") is False,
        "core Personality distinctions and candidate-only contract are frozen",
    )

    guards = boundary.get("candidate_boundary", {})
    add(
        "candidate_boundary_frozen",
        guards.get("candidate_only") is True
        and guards.get("activated") is False
        and guards.get("persisted") is False
        and guards.get("truth_declared") is False
        and guards.get("source_owner_mutation") is False
        and guards.get("fact_admission") is False,
        "candidate boundary remains non-activated, non-persistent, and non-authoritative",
    )

    negative_path = IMPLEMENTATION_DIR / "personality_governance_negative_guards_v1.json"
    negative = _json(negative_path) if negative_path.is_file() else {}
    negative_guards = negative.get("guards", {})
    add(
        "negative_guards_preserved",
        negative_guards.get("synthetic_only") is True
        and negative_guards.get("candidate_only") is True
        and all(value is False for key, value in negative_guards.items() if key not in {"synthetic_only", "candidate_only"}),
        "controlled implementation negative guards remain closed",
    )

    deferred = documents.get("personality_governance_frozen_deferred_registry_v1.json", {})
    deferred_items = {item.get("item") for item in deferred.get("deferred_items", []) if isinstance(item, dict)}
    frozen_flags = deferred.get("frozen_flags", {})
    add(
        "deferred_registry_frozen",
        deferred.get("classification") == "D"
        and deferred_items == EXPECTED_DEFERRED
        and frozen_flags.get("semantic_compression_status") == "DEFERRED_TO_EMOTION_ENGINE"
        and all(value is False for key, value in frozen_flags.items() if key != "semantic_compression_status"),
        "deferred work remains deliberately outside Personality Governance",
    )

    planning_suite_path = PLANNING_DIR / "personality_minimum_scenario_suite_v1.json"
    planning_suite = _json(planning_suite_path) if planning_suite_path.is_file() else {}
    add(
        "scenario_baseline_frozen",
        planning_suite.get("scenario_count") == 36
        and set(planning_suite.get("scenario_ids", [])) == EXPECTED_SCENARIOS
        and manifest.get("verification_baseline", {}).get("scenario_count") == 36,
        "P01-P36 is the frozen scenario baseline",
    )

    result_path = EVAL_DIR / "personality_governance_result_v1.json"
    cases_path = EVAL_DIR / "personality_governance_case_results_v1.json"
    result = _json(result_path) if result_path.is_file() else {}
    cases = _json(cases_path) if cases_path.is_file() else []
    case_ids = {item.get("scenario_id") for item in cases if isinstance(item, dict)}
    add(
        "terminal_runner_evidence",
        result.get("scenario_count") == 36
        and result.get("all_cases_passed") is True
        and result.get("failed_case_ids") == []
        and case_ids == EXPECTED_SCENARIOS
        and all(item.get("all_checks_passed") is True for item in cases),
        "existing user-terminal Runner artifacts support the frozen baseline",
    )

    terminal_claim = manifest.get("verification_baseline", {}).get("terminal_verification_evidence", {})
    add(
        "terminal_verifier_evidence",
        terminal_claim.get("source") == "user_terminal_verification_report"
        and terminal_claim.get("verifier_passed_check_count") == 22
        and terminal_claim.get("verifier_failed_check_count") == 0
        and terminal_claim.get("verifier_blocker_count") == 0,
        "user-reported controlled verifier baseline is recorded as 22/22 with no blockers",
    )

    add(
        "implementation_scope_closed",
        manifest.get("change_scope", {}).get("implementation_files_modified") == []
        and manifest.get("change_scope", {}).get("planning_assets_modified") == []
        and manifest.get("change_scope", {}).get("existing_owner_modules_modified") == [],
        "freeze records no implementation, planning, or existing-owner mutation",
    )

    phase = documents.get("phase_contract.json", {})
    add(
        "phase_contract",
        phase.get("Phase") == "Phase-Luna-Personality-Governance-Baseline-Freeze-v1-001"
        and phase.get("Execution Mode") == "BASELINE_FREEZE"
        and phase.get("Baseline Assertions", {}).get("freeze_status") == "FROZEN_V1",
        "freeze phase contract is bounded and explicit",
    )

    add(
        "no_capability_expansion",
        manifest.get("scope_rule") == "Freeze and closure only; no new Personality capability is introduced."
        and phase.get("Forbidden Scope", [])
        and "add Personality capability" in phase.get("Forbidden Scope", [])
        and phase.get("Verification Authority", {}).get("runner_execution") == "NOT_PERFORMED_IN_FREEZE",
        "freeze is closure-only and does not rerun or expand implementation",
    )

    failures = [item["name"] for item in checks if not item["passed"]]
    return {
        "FREEZE_STATUS": "FROZEN_V1" if not failures else "FROZEN_V1_BLOCKED",
        "FAILED_CHECKS": failures,
        "PASSED_CHECK_COUNT": sum(1 for item in checks if item["passed"]),
        "FAILED_CHECK_COUNT": len(failures),
        "BLOCKER_COUNT": len(failures),
        "NEXT": "WAITING_FOR_USER_TERMINAL_VERIFICATION" if not failures else "PERSONALITY_GOVERNANCE_BASELINE_FREEZE_REMEDIATION",
        "CHECKS": {item["name"]: ("pass" if item["passed"] else "fail") for item in checks},
        "DETAILS": [{"name": item["name"], "detail": item["detail"]} for item in checks],
    }


if __name__ == "__main__":
    print(json.dumps(run_verification(), indent=2, ensure_ascii=False))
