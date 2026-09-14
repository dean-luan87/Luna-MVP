"""Read-only static contract checks used by the final closure audit."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


STATIC_CONTRACTS = {
    "execution_mode": (
        "capabilities/midplatform/core/execution_mode_v1.py",
        ("SYNTHETIC_CONTROLLED", "CONTROLLED_REPLAY_RUNTIME", "LIVE_RUNTIME"),
    ),
    "a_route_request": (
        "capabilities/midplatform/core/a_route_orchestration/a_route_orchestration_core_types_v1.py",
        ("class ARouteOrchestrationRequestV1", "role_refs", "task_refs", "goal_refs", "information_need_refs"),
    ),
    "cstate_input": (
        "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_io_types_v1.py",
        ("class CognitiveStateFormationInputV1", "role_refs", "task_refs", "goal_refs", "information_need_refs"),
    ),
    "cstate_output": (
        "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_io_types_v1.py",
        ("class CognitiveStateFormationOutputV1", "evidence_relevance_candidates", "relation_interpretation_candidates"),
    ),
    "current_world": (
        "capabilities/midplatform/core/cognitive_state_formation/current_world_types_v1.py",
        ("class CurrentWorldCandidateV1", "evidence_relevance_refs", "relation_interpretation_refs"),
    ),
    "conditioning_candidates": (
        "capabilities/midplatform/core/cognitive_state_formation/cognitive_conditioning_types_v1.py",
        ("class CognitiveEvidenceRelevanceCandidateV1", "class CognitiveRelationInterpretationCandidateV1"),
    ),
    "decision_governance": (
        "capabilities/midplatform/core/decision_governance/decision_governance_engine_v1.py",
        ("class DecisionGovernanceEngineV1", "DecisionCandidateV1"),
    ),
    "task_manager": (
        "capabilities/midplatform/core/task_manager/module/task_manager_module_types_v1.py",
        ("class TaskManagerModuleRequestV1", "class TaskManagerModuleResultV1", "trace_ref"),
    ),
    "action_governance": (
        "capabilities/midplatform/core/action_governance/action_governance_engine_v1.py",
        ("class ActionGovernanceEngineV1", "runtime_handoff", "action_candidate"),
    ),
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_static_contract_audit(repo_root: Path | None = None) -> Dict[str, Any]:
    root = repo_root or _repo_root()
    checks = []
    for check_id, (relative_path, required_tokens) in STATIC_CONTRACTS.items():
        path = root / relative_path
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            checks.append({
                "check_id": check_id,
                "path": relative_path,
                "passed": False,
                "missing": list(required_tokens),
                "error": type(exc).__name__,
            })
            continue
        missing = [token for token in required_tokens if token not in text]
        checks.append({
            "check_id": check_id,
            "path": relative_path,
            "passed": not missing,
            "missing": missing,
        })

    cstate_path = root / "capabilities/midplatform/core/cognitive_state_formation/cognitive_state_formation_engine_v1.py"
    try:
        cstate_text = cstate_path.read_text(encoding="utf-8")
        controlled_replay_conditioning = (
            "if self._is_conditioned_replay(request):" in cstate_text
            and "request.role_refs" in cstate_text
            and "request.task_refs" in cstate_text
            and "request.goal_refs" in cstate_text
            and "request.information_need_refs" in cstate_text
        )
        scenario_id_is_identifier_surface = (
            "request.scenario_id" in cstate_text
            and "f\"relevance:{request.scenario_id}:" in cstate_text
            and "f\"trace:{request.scenario_id}:" in cstate_text
        )
    except (OSError, UnicodeDecodeError):
        controlled_replay_conditioning = False
        scenario_id_is_identifier_surface = False
    checks.extend(
        [
            {
                "check_id": "controlled_replay_conditioning_surface",
                "passed": controlled_replay_conditioning,
            },
            {
                "check_id": "scenario_id_identifier_surface_present",
                "passed": scenario_id_is_identifier_surface,
                "interpretation": "scenario_id remains available for IDs/traces; semantic comparisons are data-driven",
            },
        ]
    )
    return {
        "checks": checks,
        "passed": all(item.get("passed") is True for item in checks),
    }

