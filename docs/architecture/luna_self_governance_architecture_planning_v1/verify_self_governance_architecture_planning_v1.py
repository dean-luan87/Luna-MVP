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
        "self_governance_architecture_plan_v1.md",
        "self_governance_existing_asset_inventory_v1.json",
        "self_governance_owner_boundary_v1.json",
        "self_concept_boundary_matrix_v1.json",
        "self_reference_schema_v1.json",
        "self_attribution_candidate_schema_v1.json",
        "self_continuity_candidate_schema_v1.json",
        "self_boundary_classification_v1.json",
        "self_stability_mutability_model_v1.json",
        "self_attribution_state_model_v1.json",
        "self_revision_revocation_model_v1.json",
        "self_pcn_boundary_v1.json",
        "self_memory_boundary_v1.json",
        "self_learning_boundary_v1.json",
        "self_intent_boundary_v1.json",
        "self_dynamic_regulation_boundary_v1.json",
        "self_personality_boundary_v1.json",
        "self_emotion_boundary_v1.json",
        "self_privacy_sensitivity_boundary_v1.json",
        "self_trace_provenance_contract_v1.json",
        "self_idempotency_contract_v1.json",
        "self_negative_guards_v1.json",
        "self_minimum_scenario_suite_v1.json",
        "self_gap_registry_v1.json",
        "self_deferred_registry_v1.json",
        "phase_contract.json",
        "verify_self_governance_architecture_planning_v1.py",
    }


def _load_json(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return value


def run_verification() -> Dict[str, Any]:
    results: List[CheckResult] = []

    actual = {path.name for path in PHASE_DIR.iterdir() if path.is_file()}
    required = _required_files()
    results.append(
        _expect(
            actual == required,
            "P01_exact_required_file_set",
            "Exact required planning file set present.",
            f"Mismatch. missing={sorted(required - actual)} extra={sorted(actual - required)}",
        )
    )

    json_failures: List[str] = []
    docs: Dict[str, Dict[str, Any]] = {}
    for name in sorted(
        file_name for file_name in required if file_name.endswith(".json")
    ):
        try:
            docs[name] = _load_json(PHASE_DIR / name)
        except Exception as exc:
            json_failures.append(f"{name}:{exc}")
            docs[name] = {}
    results.append(
        _expect(
            not json_failures,
            "P02_json_parse",
            "All planning JSON files parse.",
            f"JSON parse failures: {json_failures}",
        )
    )

    ast_failures: List[str] = []
    try:
        ast.parse(
            (
                PHASE_DIR / "verify_self_governance_architecture_planning_v1.py"
            ).read_text(encoding="utf-8")
        )
    except Exception as exc:
        ast_failures.append(str(exc))
    results.append(
        _expect(
            not ast_failures,
            "P03_ast_parse",
            "Verifier AST parse passed.",
            f"AST parse failures: {ast_failures}",
        )
    )

    phase_contract = docs.get("phase_contract.json", {})
    flags = phase_contract.get("boundary_flags", {})
    expected_false = [
        "runtime_execution",
        "database_write",
        "vector_store_write",
        "embedding_execution",
        "model_call",
        "scheduler_execution",
        "task_mutation",
        "device_control",
        "source_owner_mutation",
        "memory_mutation",
        "learning_execution",
        "personality_mutation",
        "emotion_mutation",
        "semantic_compression_execution",
        "real_side_effect",
    ]
    results.append(
        _expect(
            phase_contract.get("Execution Mode") == "Planning Only"
            and flags.get("planning_only") is True
            and flags.get("audit_only") is True
            and all(flags.get(name) is False for name in expected_false),
            "P04_phase_contract_boundary_flags",
            "Phase contract boundary flags match planning-only rules.",
            f"Phase contract mismatch: execution_mode={phase_contract.get('Execution Mode')} flags={flags}",
        )
    )

    inventory = docs.get("self_governance_existing_asset_inventory_v1.json", {})
    owner = docs.get("self_governance_owner_boundary_v1.json", {})
    results.append(
        _expect(
            inventory.get("equivalent_current_canonical_self_owner_found") is False
            and owner.get("canonical_owner_candidate") == "Self Governance"
            and owner.get("owner_required") is True,
            "P05_owner_decision",
            "Self owner decision is coherent and narrow.",
            f"Owner decision mismatch: inventory={inventory.get('equivalent_current_canonical_self_owner_found')} owner={owner.get('canonical_owner_candidate')}",
        )
    )

    concept = docs.get("self_concept_boundary_matrix_v1.json", {})
    reference = docs.get("self_reference_schema_v1.json", {})
    attribution = docs.get("self_attribution_candidate_schema_v1.json", {})
    continuity = docs.get("self_continuity_candidate_schema_v1.json", {})
    results.append(
        _expect(
            len(concept.get("assertions", [])) >= 10
            and reference.get("schema_version") == "self-reference-schema-v1"
            and len(attribution.get("attribution_domains", [])) >= 10
            and continuity.get("schema_version") == "self-continuity-schema-v1",
            "P06_reference_attribution_continuity_models",
            "Reference, attribution, and continuity models are complete.",
            f"Model mismatch: concept={len(concept.get('assertions', []))} attribution_domains={len(attribution.get('attribution_domains', []))}",
        )
    )

    boundary = docs.get("self_boundary_classification_v1.json", {})
    stability = docs.get("self_stability_mutability_model_v1.json", {})
    state_model = docs.get("self_attribution_state_model_v1.json", {})
    revision = docs.get("self_revision_revocation_model_v1.json", {})
    results.append(
        _expect(
            len(boundary.get("classes", [])) == 7
            and len(stability.get("partitions", [])) == 4
            and len(state_model.get("states", [])) == 9
            and revision.get("supported_lineage", {}).get("revision") is True,
            "P07_boundary_state_and_revision_models",
            "Boundary classes, stability partitions, state model, and revision model are complete.",
            f"Boundary/state mismatch: classes={len(boundary.get('classes', []))} partitions={len(stability.get('partitions', []))} states={len(state_model.get('states', []))}",
        )
    )

    pcn = docs.get("self_pcn_boundary_v1.json", {})
    memory = docs.get("self_memory_boundary_v1.json", {})
    learning = docs.get("self_learning_boundary_v1.json", {})
    intent = docs.get("self_intent_boundary_v1.json", {})
    regulation = docs.get("self_dynamic_regulation_boundary_v1.json", {})
    personality = docs.get("self_personality_boundary_v1.json", {})
    emotion = docs.get("self_emotion_boundary_v1.json", {})
    results.append(
        _expect(
            pcn.get("pcn_owner_preserved") == "Personal Cognitive Network Governance"
            and memory.get("semantic_compression") == "DEFERRED_TO_EMOTION_ENGINE"
            and learning.get("frozen_assertions", {}).get(
                "learning_must_not_directly_mutate_self"
            )
            is True
            and intent.get("intent_owner_preserved") == "Intent Governance"
            and regulation.get("dynamic_regulation_owner_preserved")
            == "Dynamic Cognitive Regulation Governance"
            and personality.get("future_owner") == "Personality Governance"
            and "EmotionEvidenceToSelfCandidate"
            in emotion.get("future_evidence_interfaces", []),
            "P08_inter_owner_boundaries",
            "PCN/Memory/Learning/Intent/Regulation/Personality/Emotion boundaries are coherent.",
            "Inter-owner boundary mismatch.",
        )
    )

    privacy = docs.get("self_privacy_sensitivity_boundary_v1.json", {})
    trace = docs.get("self_trace_provenance_contract_v1.json", {})
    idem = docs.get("self_idempotency_contract_v1.json", {})
    guards = docs.get("self_negative_guards_v1.json", {})
    results.append(
        _expect(
            len(privacy.get("sensitivity_levels", [])) == 7
            and trace.get("rules", {}).get("reverse_lookup_supported") is True
            and all(bool(value) for value in idem.get("guards", {}).values())
            and guards.get("guards", {}).get("planning_only") is True,
            "P09_privacy_trace_idempotency_guards",
            "Privacy, trace/provenance, idempotency, and negative guards are complete.",
            "Privacy/trace/idempotency/guard mismatch.",
        )
    )

    scenarios = docs.get("self_minimum_scenario_suite_v1.json", {})
    gaps = docs.get("self_gap_registry_v1.json", {})
    deferred = docs.get("self_deferred_registry_v1.json", {})
    results.append(
        _expect(
            scenarios.get("scenario_count") == 34
            and gaps.get("counts", {}).get("D") >= 10
            and len(deferred.get("deferred_items", [])) >= 10,
            "P10_scenarios_gaps_deferred",
            "Scenario suite, gap registry, and deferred registry are complete.",
            f"Scenario/gap/deferred mismatch: scenarios={scenarios.get('scenario_count')} gaps={gaps.get('counts')} deferred={len(deferred.get('deferred_items', []))}",
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
        "NEXT": "SELF_GOVERNANCE_ARCHITECTURE_PLANNING_READY"
        if all_passed
        else "LUNA_SELF_GOVERNANCE_ARCHITECTURE_PLANNING_REMEDIATION",
        "DETAILS": [
            {"check_id": item.check_id, "detail": item.detail} for item in results
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_verification(), indent=2, ensure_ascii=False))
