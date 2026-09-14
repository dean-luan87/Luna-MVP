"""Summary adapter for the lifecycle closure candidate-only phase."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from .cognitive_loop_lifecycle_closure_engine_v1 import NEGATIVE_GUARDS, PHASE, build_lifecycle_closure_results_v1
from .cognitive_loop_lifecycle_closure_fixture_v1 import build_lifecycle_closure_scenario_specs_v1


CANONICAL_OWNER = "Cognitive Flow Governance"
PACKAGE_DIR = Path(__file__).resolve().parent
PLANNING_DIR_NAME = "phase_luna_dynamic_cognitive_flow_governed_multi_loop_observation_planning_v1"
REQUIRED_SOURCE_NAMES = (
    "cognitive_loop_continuity_candidate_types_v1.py",
    "cognitive_loop_continuity_candidate_engine_v1.py",
    "cognitive_loop_lifecycle_closure_types_v1.py",
    "cognitive_loop_lifecycle_closure_fixture_v1.py",
    "cognitive_loop_lifecycle_closure_engine_v1.py",
    "cognitive_loop_lifecycle_closure_adapter_v1.py",
    "run_cognitive_loop_lifecycle_closure_and_assimilation_bridge_controlled_implementation_v1.py",
    "verify_cognitive_loop_lifecycle_closure_and_assimilation_bridge_controlled_implementation_v1.py",
)
REQUIRED_DOCUMENT_NAMES = (
    "lifecycle_closure_contract_v1.md",
    "closure_reason_mapping_v1.md",
    "final_state_integrity_and_requirement_disposition_v1.md",
    "brain_assimilation_and_loop_package_boundary_v1.md",
    "scenario_mapping_v1.json",
    "change_manifest.md",
)


def _repository_root() -> Path:
    for parent in PACKAGE_DIR.parents:
        if (parent / "docs" / "architecture").is_dir():
            return parent
    return PACKAGE_DIR


def planning_dir() -> Path:
    return _repository_root() / "docs" / "architecture" / PLANNING_DIR_NAME


def source_set_ok() -> bool:
    return all((PACKAGE_DIR / name).is_file() for name in REQUIRED_SOURCE_NAMES)


def documentation_set_ok() -> bool:
    return all((planning_dir() / name).is_file() for name in REQUIRED_DOCUMENT_NAMES)


def _failed_checks(result) -> Tuple[str, ...]:
    return tuple(f"{result.scenario_id}:{name}" for name, passed in result.checks if not passed)


def build_lifecycle_closure_run_v1() -> Dict[str, Any]:
    specs = build_lifecycle_closure_scenario_specs_v1()
    results = build_lifecycle_closure_results_v1(specs)
    failed_case_ids = [result.scenario_id for result in results if _failed_checks(result)]
    failed_checks = [check for result in results for check in _failed_checks(result)]
    negative_guards_ok = all(
        all(name in NEGATIVE_GUARDS and value is False for name, value in result.negative_guards)
        for result in results
    )
    lifecycle_closure_ok = all(
        result.lifecycle_closure.accepted == (result.lifecycle_closure.target_closure_state == "CLOSED")
        and result.closure_assessment.local_closure_state == "OPEN"
        for result in results
    )
    final_state_integrity_ok = all(
        (result.final_state_freeze is not None and result.final_state_freeze.final_state_frozen)
        == result.lifecycle_closure.accepted
        for result in results
    )
    brain_assimilation_boundary_ok = all(
        result.assimilation is None
        or (
            result.assimilation.candidate_only
            and not result.assimilation.world_truth_declared
            and not result.assimilation.action_executed
            and not result.assimilation.memory_mutation
            and not result.assimilation.experience_mutation
            and not result.assimilation.learning_executed
            and not result.assimilation.automatic_loop_generation
        )
        for result in results
    )
    loop_package_boundary_ok = all(
        result.loop_package is None
        or (
            result.loop_package.candidate_only
            and not result.loop_package.semantic_compression
            and not result.loop_package.authoritative_state_copied
            and result.history_boundary.runtime_history_preserved
        )
        for result in results
    )
    key_guards = {
        "candidate_only": all(result.candidate_only for result in results),
        "closure_acceptance_brain_governed": all(result.closure_decision.governing_owner_ref == "brain:cognitive-flow-governance" for result in results),
        "closure_candidate_not_acceptance": all(not result.closure_assessment.lifecycle_closure_accepted for result in results),
        "final_state_frozen_only_after_acceptance": final_state_integrity_ok,
        "stale_requirement_direct_invocation": False,
        "post_closure_requirement_invocation": False,
        "skipped_candidates_not_failures": all(any(name == "skipped_candidates_not_failures" and passed for name, passed in result.checks) for result in results),
        "loop_self_authorized_closure": False,
        "loop_self_assimilation": False,
        "autonomous_loop_spawning": False,
        "semantic_compression": False,
    }
    return {
        "phase": PHASE,
        "canonical_owner": CANONICAL_OWNER,
        "scenario_count": len(results),
        "all_cases_passed": not failed_case_ids,
        "failed_case_ids": failed_case_ids,
        "failed_checks": failed_checks,
        "candidate_only": True,
        "synthetic_only": True,
        "runtime_execution": False,
        "provider_invocation": False,
        "model_inference": False,
        "lifecycle_closure_ok": lifecycle_closure_ok,
        "final_state_integrity_ok": final_state_integrity_ok,
        "brain_assimilation_boundary_ok": brain_assimilation_boundary_ok,
        "loop_package_boundary_ok": loop_package_boundary_ok,
        "negative_guards_ok": negative_guards_ok,
        "negative_guards": dict(NEGATIVE_GUARDS),
        "key_guards": key_guards,
        "negative_guard_count": len(NEGATIVE_GUARDS),
        "source_set_ok": source_set_ok(),
        "documentation_set_ok": documentation_set_ok(),
    }


__all__ = [
    "PHASE",
    "CANONICAL_OWNER",
    "REQUIRED_SOURCE_NAMES",
    "REQUIRED_DOCUMENT_NAMES",
    "planning_dir",
    "source_set_ok",
    "documentation_set_ok",
    "build_lifecycle_closure_run_v1",
]
