"""User-terminal static verifier for Emotion Governance architecture planning."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any, Dict, List, Set


def _find_repo_root(start: Path) -> Path:
    """Walk upward to stable repository sentinels without depending on cwd."""
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
CODE_DIR = REPO_ROOT / "capabilities/midplatform/core/emotion_governance"
REQUIRED_FILES: Set[str] = {
    "emotion_governance_architecture_plan_v1.md",
    "emotion_governance_existing_asset_inventory_v1.json",
    "emotion_governance_owner_boundary_v1.json",
    "emotion_concept_boundary_matrix_v1.json",
    "emotion_evidence_candidate_schema_v1.json",
    "emotion_appraisal_candidate_schema_v1.json",
    "emotion_state_candidate_schema_v1.json",
    "emotion_state_taxonomy_v1.json",
    "emotion_state_lifecycle_model_v1.json",
    "emotion_temporal_dynamics_contract_v1.json",
    "emotion_conflict_mixed_state_model_v1.json",
    "emotion_self_boundary_v1.json",
    "emotion_personality_boundary_v1.json",
    "emotion_memory_experience_boundary_v1.json",
    "emotion_learning_boundary_v1.json",
    "emotion_intent_boundary_v1.json",
    "emotion_attention_boundary_v1.json",
    "emotion_dynamic_regulation_boundary_v1.json",
    "emotion_pcn_relationship_boundary_v1.json",
    "emotion_semantic_compression_ownership_decision_v1.json",
    "emotion_privacy_sensitivity_boundary_v1.json",
    "emotion_trace_provenance_contract_v1.json",
    "emotion_idempotency_contract_v1.json",
    "emotion_revision_revocation_model_v1.json",
    "emotion_negative_guards_v1.json",
    "emotion_minimum_scenario_suite_v1.json",
    "emotion_gap_registry_v1.json",
    "emotion_deferred_registry_v1.json",
    "phase_contract.json",
    "verify_emotion_governance_architecture_planning_v1.py",
}
JSON_FILES = {name for name in REQUIRED_FILES if name.endswith(".json")}
EXPECTED_SCENARIOS = {f"E{index:02d}" for index in range(1, 37)}
EXPECTED_STATES = {
    "PROPOSED", "EVIDENCE_ACCUMULATING", "INSUFFICIENT_EVIDENCE", "CONTESTED", "MIXED",
    "TEMPORARY", "ACTIVE_CANDIDATE", "DECAYING", "RECOVERING", "REVISED", "SUPERSEDED",
    "REVOKED", "EXPIRED",
}
EXPECTED_SENSITIVITY = {
    "NORMAL", "SENSITIVE", "HIGH_SENSITIVITY", "USER_CONFIRMATION_REQUIRED",
    "DO_NOT_GENERALIZE", "DO_NOT_TRANSFER", "DO_NOT_PERSIST_CANDIDATE",
}
EXPECTED_FOUR_DEFERRED = {
    "semantic compression",
    "affective memory compression",
    "emotion-memory summary",
    "personality-memory semantic fusion",
}
REQUIRED_FALSE_GUARDS = {
    "emotion_can_mutate_self", "emotion_can_mutate_personality", "emotion_can_mutate_memory",
    "emotion_can_execute_learning", "emotion_can_mutate_intent", "emotion_can_mutate_attention",
    "emotion_can_mutate_pcn", "emotion_can_mutate_current_world", "emotion_can_mutate_state_vector",
    "emotion_can_mutate_regulation_parameters", "emotion_can_activate_parameter_genome",
    "emotion_can_create_task", "emotion_can_control_device", "emotion_can_run_scheduler",
    "emotion_can_call_model", "database_write", "vector_store_write", "embedding_execution",
    "runtime_execution", "source_owner_mutation", "cross_user_transfer", "real_side_effect",
    "semantic_compression_execution", "affective_memory_compression_execution",
    "emotion_memory_summary_generation", "personality_memory_semantic_fusion", "emotion_runtime",
    "emotion_model_inference", "emotion_expression_execution",
}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_verification() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    actual_files = {path.name for path in PHASE_DIR.iterdir() if path.is_file()}
    add("exact_required_files", actual_files == REQUIRED_FILES, f"missing={sorted(REQUIRED_FILES - actual_files)} extra={sorted(actual_files - REQUIRED_FILES)}")

    documents: Dict[str, Any] = {}
    json_failures: List[str] = []
    for name in sorted(JSON_FILES):
        try:
            documents[name] = _json(PHASE_DIR / name)
        except Exception as exc:
            json_failures.append(f"{name}:{exc}")
            documents[name] = {}
    add("json_parse", not json_failures, str(json_failures) if json_failures else "all planning JSON parsed")

    ast_failures: List[str] = []
    try:
        ast.parse((PHASE_DIR / "verify_emotion_governance_architecture_planning_v1.py").read_text(encoding="utf-8"))
    except Exception as exc:
        ast_failures.append(str(exc))
    add("verifier_ast_parse", not ast_failures, str(ast_failures) if ast_failures else "planning verifier AST parsed")

    phase = documents.get("phase_contract.json", {})
    flags = phase.get("boundary_flags", {})
    add("planning_only_boundary", phase.get("Execution Mode") == "PLANNING_ONLY" and flags.get("planning_only") is True and all(value is False for key, value in flags.items() if key != "planning_only"), "planning-only and all side-effect/mutation flags are closed")
    add("no_emotion_implementation_module", not CODE_DIR.exists(), "emotion_governance implementation directory is absent")

    owner = documents.get("emotion_governance_owner_boundary_v1.json", {})
    inventory = documents.get("emotion_governance_existing_asset_inventory_v1.json", {})
    add("canonical_owner_decision", owner.get("canonical_owner") == "Emotion Governance" and owner.get("equivalent_existing_owner") is False and inventory.get("canonical_owner_exists_before_phase") is False, "one new canonical planning owner selected after audit")

    matrix = documents.get("emotion_concept_boundary_matrix_v1.json", {})
    inequalities = set(matrix.get("frozen_inequalities", []))
    required_inequalities = {
        "Emotion Evidence != Emotion Appraisal", "Emotion Appraisal != Emotion State", "Emotion State != Mood",
        "Emotion State != Personality Trait", "Emotion State != Self", "Emotion State != Memory",
        "Emotion State != Intent", "Emotion State != Action", "Emotion State != External Reality",
    }
    add("conceptual_inequalities", required_inequalities.issubset(inequalities), "all required conceptual distinctions are frozen")

    lifecycle = documents.get("emotion_state_lifecycle_model_v1.json", {})
    add("lifecycle_completeness", set(lifecycle.get("states", [])) == EXPECTED_STATES and bool(lifecycle.get("transitions")), "lifecycle states and transitions are defined")

    temporal = documents.get("emotion_temporal_dynamics_contract_v1.json", {})
    temporal_ops = temporal.get("temporal_operations", {})
    add("temporal_dynamics", all(name in temporal_ops for name in {"accumulation", "decay", "persistence_candidate", "recovery", "refresh", "repeated_stimulus", "temporal_validity", "stale_expiration"}) and temporal.get("invariants", {}).get("no_hidden_permanent_emotion_state") is True, "temporal accumulation, decay, refresh, recovery, validity, and no-permanent-state rules exist")

    conflict = documents.get("emotion_conflict_mixed_state_model_v1.json", {})
    conflict_rules = conflict.get("representation_rules", {})
    add("mixed_conflict_preservation", all(conflict_rules.get(key) is True for key in {"contradictory_evidence_preserved", "mixed_emotion_refs_preserved", "competing_state_refs_preserved", "unresolved_attribution_preserved", "uncertainty_preserved", "no_silent_averaging", "no_forced_single_category"}), "mixed, competing, contradictory, and unresolved candidates are retained")

    boundary_files = [
        "emotion_self_boundary_v1.json", "emotion_personality_boundary_v1.json", "emotion_memory_experience_boundary_v1.json",
        "emotion_learning_boundary_v1.json", "emotion_intent_boundary_v1.json", "emotion_attention_boundary_v1.json",
        "emotion_dynamic_regulation_boundary_v1.json", "emotion_pcn_relationship_boundary_v1.json",
    ]
    boundary_text = "\n".join((PHASE_DIR / name).read_text(encoding="utf-8") for name in boundary_files)
    add("inter_owner_boundaries", all(term in boundary_text for term in ["candidate_only", "mutation", "Personality", "Memory", "Learning", "Intent", "Attention", "Regulation", "PCN"]), "all required cross-owner boundary assets exist")
    add("personality_freeze_preserved", documents.get("emotion_personality_boundary_v1.json", {}).get("personality_baseline_status") == "FROZEN_V1" and documents.get("emotion_personality_boundary_v1.json", {}).get("frozen_rules", {}).get("personality_governance_remains_frozen") is True, "Personality Governance FROZEN_V1 is preserved")

    compression = documents.get("emotion_semantic_compression_ownership_decision_v1.json", {})
    decisions = {item.get("capability") for item in compression.get("decisions", []) if isinstance(item, dict)}
    compression_flags = compression.get("frozen_flags", {})
    add("semantic_compression_ownership_decision", decisions == EXPECTED_FOUR_DEFERRED and compression_flags.get("emotion_governance_owns_all_four") is False and all(value is False for key, value in compression_flags.items() if key != "emotion_governance_owns_all_four"), "all four ownership decisions are explicit and deferred without convenience assignment")

    privacy = documents.get("emotion_privacy_sensitivity_boundary_v1.json", {})
    add("privacy_sensitivity", set(privacy.get("levels", [])) == EXPECTED_SENSITIVITY and privacy.get("rules", {}).get("cross_user_transfer") is False, "all sensitivity levels and transfer restriction are present")

    trace = documents.get("emotion_trace_provenance_contract_v1.json", {})
    add("trace_provenance", all(term in trace.get("reverse_route", []) for term in ["Emotion State Candidate", "Emotion Appraisal Candidate", "Emotion Evidence Candidate", "Cognitive Cycle", "original source evidence"]) and trace.get("rules", {}).get("reverse_lookup_supported") is True and trace.get("rules", {}).get("provenance_does_not_grant_semantic_authority") is True, "reverse trace and authority-free provenance are defined")

    idem = documents.get("emotion_idempotency_contract_v1.json", {})
    add("idempotency", all(term in idem.get("guards", []) for term in ["duplicate_emotion_evidence_guard", "duplicate_emotion_appraisal_guard", "duplicate_emotion_state_formation_guard", "duplicate_emotion_refresh_guard", "revision_replay_guard", "revocation_replay_guard", "expiration_replay_guard"]), "duplicate and lifecycle replay guards are defined")

    negative = documents.get("emotion_negative_guards_v1.json", {}).get("guards", {})
    add("negative_guards", REQUIRED_FALSE_GUARDS.issubset(negative) and all(negative.get(name) is False for name in REQUIRED_FALSE_GUARDS) and negative.get("planning_only") is True, "required negative guards are frozen false")

    suite = documents.get("emotion_minimum_scenario_suite_v1.json", {})
    add("scenario_coverage", suite.get("scenario_count") == 36 and set(suite.get("scenario_ids", [])) == EXPECTED_SCENARIOS and len(suite.get("scenarios", [])) == 36, "E01-E36 scenario suite is complete")

    gap = documents.get("emotion_gap_registry_v1.json", {})
    gap_classes = {item.get("classification") for item in gap.get("gaps", []) if isinstance(item, dict)}
    add("abcd_gap_registry", {"A", "B", "C", "D"}.issubset(gap_classes), "A/B/C/D gap classifications are represented")

    deferred = documents.get("emotion_deferred_registry_v1.json", {})
    deferred_items = set(deferred.get("deferred_items", []))
    add("deferred_registry", {"real Emotion Engine runtime", "emotion model inference", "persistent emotional state storage", "semantic compression execution", "affective memory compression execution", "emotion-memory summary generation", "personality-memory semantic fusion", "cross-user emotion transfer"}.issubset(deferred_items) and deferred.get("classification") == "D" and deferred.get("frozen_flags", {}).get("planning_only") is True, "runtime, model, persistence, synthesis, and transfer work remains deferred")

    failures = [item["name"] for item in checks if not item["passed"]]
    return {
        "CHECKS": {item["name"]: ("pass" if item["passed"] else "fail") for item in checks},
        "FAILED_CHECKS": failures,
        "PASSED_CHECK_COUNT": sum(1 for item in checks if item["passed"]),
        "FAILED_CHECK_COUNT": len(failures),
        "BLOCKER_COUNT": len(failures),
        "STATIC_STATUS": "PLANNING_ASSETS_READY_FOR_USER_TERMINAL_VERIFICATION" if not failures else "PLANNING_ASSETS_BLOCKED",
        "NEXT": "WAITING_FOR_USER_TERMINAL_VERIFICATION" if not failures else "LUNA_EMOTION_GOVERNANCE_ARCHITECTURE_PLANNING_REMEDIATION",
        "DETAILS": [{"name": item["name"], "detail": item["detail"]} for item in checks],
    }


if __name__ == "__main__":
    print(json.dumps(run_verification(), indent=2, ensure_ascii=False))
