from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any, Dict, List, Set

PHASE_DIR = Path(__file__).resolve().parent

REQUIRED_FILES: Set[str] = {
    "personality_governance_architecture_plan_v1.md",
    "personality_governance_existing_asset_inventory_v1.json",
    "personality_governance_owner_boundary_v1.json",
    "personality_concept_boundary_matrix_v1.json",
    "personality_trait_candidate_schema_v1.json",
    "personality_profile_candidate_schema_v1.json",
    "personality_trait_taxonomy_v1.json",
    "personality_trait_stability_model_v1.json",
    "personality_evidence_admission_model_v1.json",
    "personality_revision_revocation_model_v1.json",
    "personality_self_boundary_v1.json",
    "personality_memory_boundary_v1.json",
    "personality_learning_boundary_v1.json",
    "personality_emotion_boundary_v1.json",
    "personality_dynamic_regulation_boundary_v1.json",
    "personality_pcn_boundary_v1.json",
    "personality_intent_boundary_v1.json",
    "personality_privacy_sensitivity_boundary_v1.json",
    "personality_trace_provenance_contract_v1.json",
    "personality_idempotency_contract_v1.json",
    "personality_semantic_compression_deferred_boundary_v1.json",
    "personality_negative_guards_v1.json",
    "personality_minimum_scenario_suite_v1.json",
    "personality_gap_registry_v1.json",
    "personality_deferred_registry_v1.json",
    "phase_contract.json",
    "verify_personality_governance_architecture_planning_v1.py",
}

JSON_FILES = {name for name in REQUIRED_FILES if name.endswith(".json")}


def _load_json(name: str) -> Dict[str, Any]:
    value = json.loads((PHASE_DIR / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{name} must contain an object")
    return value


def run_static_review() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    def add(name: str, condition: bool, detail: str) -> None:
        checks.append({"name": name, "ok": bool(condition), "detail": detail})

    actual = {path.name for path in PHASE_DIR.iterdir() if path.is_file()}
    add("exact_required_file_set", actual == REQUIRED_FILES, f"missing={sorted(REQUIRED_FILES - actual)} extra={sorted(actual - REQUIRED_FILES)}")

    docs: Dict[str, Dict[str, Any]] = {}
    parse_failures: List[str] = []
    for name in sorted(JSON_FILES):
        try:
            docs[name] = _load_json(name)
        except Exception as exc:
            parse_failures.append(f"{name}:{exc}")
            docs[name] = {}
    add("json_assets_parse", not parse_failures, str(parse_failures) if parse_failures else "all planning JSON parsed")

    ast_failures: List[str] = []
    try:
        ast.parse((PHASE_DIR / "verify_personality_governance_architecture_planning_v1.py").read_text(encoding="utf-8"))
    except Exception as exc:
        ast_failures.append(str(exc))
    add("verifier_ast_parse", not ast_failures, str(ast_failures) if ast_failures else "verifier AST parsed")

    contract = docs.get("phase_contract.json", {})
    flags = contract.get("boundary_flags", {})
    forbidden_true = [name for name in flags if name not in {"planning_only", "audit_only"} and flags.get(name) is True]
    add("planning_only_boundary", contract.get("Execution Mode") == "Planning Only" and flags.get("planning_only") is True and flags.get("audit_only") is True and not forbidden_true, f"execution_mode={contract.get('Execution Mode')} forbidden_true={forbidden_true}")
    add("stop_status", contract.get("Current Status Contract") == "WAITING_FOR_USER_TERMINAL_VERIFICATION" and contract.get("Agent Stop Point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "agent stops before user terminal verification")

    inventory = docs.get("personality_governance_existing_asset_inventory_v1.json", {})
    classifications = {item.get("classification") for item in inventory.get("assets", []) if isinstance(item, dict)}
    add("inventory_owner_audit", inventory.get("equivalent_current_canonical_personality_owner_found") is False and inventory.get("canonical_owner_decision") == "Personality Governance" and classifications == {"A", "B", "C", "D"}, f"owner={inventory.get('canonical_owner_decision')} classifications={sorted(classifications)}")

    owner = docs.get("personality_governance_owner_boundary_v1.json", {})
    add("single_narrow_owner", owner.get("canonical_owner") == "Personality Governance" and owner.get("equivalent_existing_owner") is False and set(owner.get("forbidden_parallel_owners", [])) == {"trait_governance", "persona_governance", "temperament_governance", "character_governance"}, "single Personality Governance owner and forbidden parallel owners recorded")

    concept = docs.get("personality_concept_boundary_matrix_v1.json", {})
    required_inequalities = {"Personality != Self", "Personality != Emotion", "Personality != Preference", "Personality != Memory", "Personality != Learning Pattern", "Personality != Dynamic Regulation Parameter", "Personality Trait Candidate != Activated Trait", "Repeated Behavior != Personality Truth", "Repeated Emotion != Personality Trait", "Temporary Regulation Pattern != Personality Trait", "User Correction > Inferred Personality Candidate", "Personality Evolution Evidence != Personality Mutation"}
    add("semantic_inequalities", required_inequalities.issubset(set(concept.get("assertions", []))) and concept.get("boundary_rules", {}).get("profile_flattening_to_single_score") is False, "required Personality inequalities and non-flattened profile rule recorded")

    trait = docs.get("personality_trait_candidate_schema_v1.json", {})
    required_trait_fields = {"trait_candidate_id", "trait_dimension", "trait_value_candidate", "source_refs", "evidence_refs", "memory_refs", "learning_refs", "self_refs", "emotion_refs", "regulation_refs", "interaction_refs", "confidence_candidate", "evidence_strength", "repetition", "context_diversity", "temporal_span", "stability_candidate", "uncertainty_refs", "contradiction_refs", "counterexample_refs", "revision_parent_ref", "supersedes_ref", "revocation_refs", "sensitivity", "trace_ref", "provenance_refs", "schema_version", "contract_version"}
    trait_flags = trait.get("invariants", {})
    add("trait_candidate_schema", required_trait_fields.issubset(set(trait.get("required_fields", []))) and all(trait_flags.get(name) is expected for name, expected in {"candidate_only": True, "activated": False, "persisted": False, "truth_declared": False}.items()), "trait schema fields and candidate-only invariants are complete")

    profile = docs.get("personality_profile_candidate_schema_v1.json", {})
    profile_rules = profile.get("profile_rules", {})
    add("profile_candidate_schema", profile_rules.get("composed_from_multiple_traits") is True and profile_rules.get("flattened_single_score") is False and profile_rules.get("uncertain_traits_allowed") is True and profile_rules.get("contested_traits_allowed") is True and profile_rules.get("contradictory_candidates_allowed") is True and profile.get("invariants", {}).get("activated") is False, "profile remains multi-trait, uncertain/contested, contradictory, and inactive")

    taxonomy = docs.get("personality_trait_taxonomy_v1.json", {})
    add("trait_taxonomy", len(taxonomy.get("candidate_dimensions", [])) >= 18 and taxonomy.get("dimension_rules", {}).get("diagnostic") is False and taxonomy.get("dimension_rules", {}).get("single_score_substitute") is False, f"dimensions={len(taxonomy.get('candidate_dimensions', []))}")

    stability = docs.get("personality_trait_stability_model_v1.json", {})
    add("stability_model", len(stability.get("states", [])) == 9 and stability.get("rules", {}).get("short_term_single_behavior_not_trait") is True and stability.get("rules", {}).get("counterexample_retained") is True and stability.get("rules", {}).get("evolution_requires_revision_lineage") is True, "stability ladder and promotion safeguards are complete")

    admission = docs.get("personality_evidence_admission_model_v1.json", {})
    add("evidence_admission", admission.get("admission_rules", {}).get("one_event_is_insufficient") is True and admission.get("admission_rules", {}).get("cross_context_requires_stricter_evidence") is True and admission.get("admission_rules", {}).get("admission_does_not_activate_trait") is True, "admission preserves evidence limits and activation boundary")

    revision = docs.get("personality_revision_revocation_model_v1.json", {})
    lineage = revision.get("supported_lineage", {})
    add("revision_lineage", all(lineage.get(name) is True for name in ["revision", "supersession", "revocation", "expiration"]) and revision.get("rules", {}).get("counterexamples_preserved") is True and revision.get("rules", {}).get("user_correction_precedence") is True, "revision, supersession, revocation, expiration, and correction lineage are present")

    boundary_names = ["personality_self_boundary_v1.json", "personality_memory_boundary_v1.json", "personality_learning_boundary_v1.json", "personality_emotion_boundary_v1.json", "personality_dynamic_regulation_boundary_v1.json", "personality_pcn_boundary_v1.json", "personality_intent_boundary_v1.json"]
    add("inter_owner_boundaries", all(name in docs for name in boundary_names) and docs.get("personality_self_boundary_v1.json", {}).get("self_owner_preserved") == "Self Governance" and docs.get("personality_memory_boundary_v1.json", {}).get("memory_owner_preserved") == "Cognitive Memory & Experience Governance" and docs.get("personality_learning_boundary_v1.json", {}).get("learning_owner_preserved") == "Cognitive Learning Governance" and docs.get("personality_pcn_boundary_v1.json", {}).get("pcn_owner_preserved") == "Personal Cognitive Network Governance" and docs.get("personality_intent_boundary_v1.json", {}).get("intent_owner_preserved") == "Intent Governance", "Self/Memory/Learning/Emotion/Regulation/PCN/Intent owners remain distinct")

    privacy = docs.get("personality_privacy_sensitivity_boundary_v1.json", {})
    add("privacy_boundary", len(privacy.get("sensitivity_levels", [])) == 7 and privacy.get("rules", {}).get("cross_user_transfer") is False and privacy.get("rules", {}).get("do_not_generalize_is_hard_boundary") is True, "seven sensitivity levels and transfer/generalization restrictions are present")

    trace = docs.get("personality_trace_provenance_contract_v1.json", {})
    add("trace_provenance", trace.get("rules", {}).get("reverse_lookup_supported") is True and trace.get("rules", {}).get("contradictions_reverse_locatable") is True and trace.get("rules", {}).get("counterexamples_reverse_locatable") is True and trace.get("rules", {}).get("provenance_grants_authority") is False, "reverse lookup and lineage preservation are required without authority transfer")

    idem = docs.get("personality_idempotency_contract_v1.json", {})
    add("idempotency", len(idem.get("guards", [])) >= 8 and idem.get("rules", {}).get("replayed_evidence_does_not_raise_stability") is True and idem.get("rules", {}).get("user_correction_cannot_be_overwritten_by_inference") is True, "duplicate/replay/correction guards are present")

    compression = docs.get("personality_semantic_compression_deferred_boundary_v1.json", {})
    add("compression_deferred", compression.get("semantic_compression_status") == "DEFERRED_TO_EMOTION_ENGINE" and compression.get("rules", {}).get("current_phase_executes_compression") is False and compression.get("rules", {}).get("future_refs_must_be_nullable") is True, "semantic compression is deferred and future refs are nullable")

    guards = docs.get("personality_negative_guards_v1.json", {}).get("guards", {})
    required_false = ["personality_can_mutate_self", "personality_can_mutate_memory", "personality_can_execute_learning", "personality_can_mutate_intent", "personality_can_mutate_pcn", "personality_can_mutate_emotion", "personality_can_mutate_regulation_parameters", "personality_can_activate_parameter_genome", "personality_can_create_task", "personality_can_control_device", "personality_can_run_scheduler", "personality_can_call_model", "database_write", "vector_store_write", "embedding_execution", "runtime_execution", "source_owner_mutation", "cross_user_transfer", "semantic_compression_execution", "real_side_effect"]
    add("negative_guards", all(guards.get(name) is False for name in required_false) and guards.get("candidate_only") is True and guards.get("planning_only") is True, "required negative guards are frozen")

    scenarios = docs.get("personality_minimum_scenario_suite_v1.json", {})
    scenario_ids = {item.get("scenario_id") for item in scenarios.get("scenarios", []) if isinstance(item, dict)}
    expected_ids = {f"P{index:02d}" for index in range(1, 37)}
    add("scenario_suite", scenarios.get("scenario_count") == 36 and scenario_ids == expected_ids and scenarios.get("coverage_rules", {}).get("candidate_only") is True and scenarios.get("coverage_rules", {}).get("no_runtime") is True, f"scenario_count={scenarios.get('scenario_count')} missing={sorted(expected_ids - scenario_ids)} extra={sorted(scenario_ids - expected_ids)}")

    gaps = docs.get("personality_gap_registry_v1.json", {})
    gap_counts: Dict[str, int] = {key: 0 for key in ["A", "B", "C", "D"]}
    for gap in gaps.get("gaps", []):
        if isinstance(gap, dict) and gap.get("classification") in gap_counts:
            gap_counts[gap["classification"]] += 1
    add("gap_registry", gaps.get("counts") == gap_counts and all(gap_counts[key] > 0 for key in gap_counts), f"declared={gaps.get('counts')} actual={gap_counts}")

    deferred = docs.get("personality_deferred_registry_v1.json", {})
    add("deferred_registry", deferred.get("classification") == "D" and len(deferred.get("deferred_items", [])) >= 10 and "Emotion Engine implementation" in deferred.get("deferred_items", []), "D registry records deliberate deferred work")

    failures = [item["name"] for item in checks if not item["ok"]]
    return {
        "CHECKS": {item["name"]: item["ok"] for item in checks},
        "FAILED_CHECKS": failures,
        "SUCCESSFUL_CHECK_COUNT": sum(1 for item in checks if item["ok"]),
        "FAILED_CHECK_COUNT": len(failures),
        "BLOCKER_COUNT": len(failures),
        "STATUS": "STATIC_CHECK_READY" if not failures else "BLOCKED_BEFORE_USER_TERMINAL_VERIFICATION",
        "NEXT": "WAITING_FOR_USER_TERMINAL_VERIFICATION" if not failures else "LUNA_PERSONALITY_GOVERNANCE_ARCHITECTURE_PLANNING_REMEDIATION",
        "DETAILS": [{"name": item["name"], "detail": item["detail"]} for item in checks],
    }


if __name__ == "__main__":
    print(json.dumps(run_static_review(), indent=2, ensure_ascii=False))
