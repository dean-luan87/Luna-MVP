#!/usr/bin/env python3
"""Read-only verifier for PCN module closure v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


DOC_DIR = Path(__file__).resolve().parent
REPO_ROOT = DOC_DIR.parents[2]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _check(condition: bool, name: str, checks: List[str], failures: List[str]) -> None:
    checks.append(name)
    if not condition:
        failures.append(name)


def main() -> int:
    checks: List[str] = []
    failures: List[str] = []

    required_assets = [
        DOC_DIR / "personal_cognitive_network_module_closure_v1.md",
        DOC_DIR / "pcn_module_baseline_v1.json",
        DOC_DIR / "pcn_owner_and_mutation_authority_closure_v1.json",
        DOC_DIR / "pcn_input_output_closure_contract_v1.json",
        DOC_DIR / "pcn_nested_constraint_closure_contract_v1.json",
        DOC_DIR / "pcn_field_role_interaction_closure_v1.json",
        DOC_DIR / "pcn_resource_boundary_closure_v1.json",
        DOC_DIR / "pcn_subjective_cognition_closure_v1.json",
        DOC_DIR / "pcn_to_intent_handoff_contract_candidate_v1.json",
        DOC_DIR / "pcn_clarification_closure_registry_v1.json",
        DOC_DIR / "pcn_existing_asset_reuse_mapping_v1.json",
        DOC_DIR / "pcn_module_closure_change_manifest_v1.json",
        DOC_DIR / "phase_contract.json",
        DOC_DIR / "verify_personal_cognitive_network_module_closure_v1.py",
    ]
    for path in required_assets:
        _check(path.is_file(), f"required_asset:{path.name}", checks, failures)

    if failures:
        _emit(checks, failures)
        return 1

    baseline = _load_json(DOC_DIR / "pcn_module_baseline_v1.json")
    owner = _load_json(DOC_DIR / "pcn_owner_and_mutation_authority_closure_v1.json")
    io_contract = _load_json(DOC_DIR / "pcn_input_output_closure_contract_v1.json")
    nested = _load_json(DOC_DIR / "pcn_nested_constraint_closure_contract_v1.json")
    interaction = _load_json(DOC_DIR / "pcn_field_role_interaction_closure_v1.json")
    resource = _load_json(DOC_DIR / "pcn_resource_boundary_closure_v1.json")
    subjective = _load_json(DOC_DIR / "pcn_subjective_cognition_closure_v1.json")
    handoff = _load_json(DOC_DIR / "pcn_to_intent_handoff_contract_candidate_v1.json")
    clar = _load_json(DOC_DIR / "pcn_clarification_closure_registry_v1.json")
    reuse = _load_json(DOC_DIR / "pcn_existing_asset_reuse_mapping_v1.json")
    manifest = _load_json(DOC_DIR / "pcn_module_closure_change_manifest_v1.json")
    phase_contract = _load_json(DOC_DIR / "phase_contract.json")

    dryrun_result = _load_json(
        REPO_ROOT
        / "_eval_out/personal_cognitive_network_controlled_dryrun_v1/pcn_controlled_dryrun_result_v1.json"
    )

    _check(
        len(baseline.get("source_stage_chain", [])) == 6,
        "source_stage_chain_complete",
        checks,
        failures,
    )
    _check(
        dryrun_result.get("case_count") == 12, "dryrun_case_count_12", checks, failures
    )
    _check(
        dryrun_result.get("failed_case_count") == 0,
        "dryrun_failed_case_count_zero",
        checks,
        failures,
    )
    _check(
        dryrun_result.get("blocker_count") == 0,
        "dryrun_blocker_count_zero",
        checks,
        failures,
    )
    _check(
        "PCN_CONTROLLED_DRYRUN_VALIDATION_PASSED"
        in "".join(baseline.get("dryrun_evidence_refs", [])),
        "dryrun_terminal_evidence_recorded",
        checks,
        failures,
    )

    _check(bool(owner.get("pcn_owner")), "owner_unique_present", checks, failures)
    _check(
        owner.get("mutation_authority_preserved") is True,
        "mutation_authority_preserved",
        checks,
        failures,
    )
    _check(owner.get("owner_changed") is False, "owner_unchanged", checks, failures)

    _check(
        "intent" in io_contract.get("forbidden_outputs", {}),
        "intent_forbidden_output_declared",
        checks,
        failures,
    )
    _check(
        io_contract.get("equivalence_guards", {}).get("pcn_activation_not_intent")
        is True,
        "pcn_activation_not_intent",
        checks,
        failures,
    )
    _check(
        io_contract.get("equivalence_guards", {}).get("strong_link_not_intent") is True,
        "strong_link_not_intent",
        checks,
        failures,
    )
    _check(
        io_contract.get("equivalence_guards", {}).get("repeated_activation_not_intent")
        is True,
        "repeated_activation_not_intent",
        checks,
        failures,
    )

    _check(
        nested.get("owner_independence_not_equal_cognitive_isolation") is True,
        "owner_independence_not_isolation",
        checks,
        failures,
    )
    _check(
        nested.get("relation_semantics", {}).get("cross_owner_mutation") is False,
        "nested_cross_owner_mutation_forbidden",
        checks,
        failures,
    )

    _check(
        interaction.get("semantic_guards", {}).get("resonance_not_causal_fact") is True,
        "resonance_not_causal",
        checks,
        failures,
    )
    _check(
        interaction.get("semantic_guards", {}).get("competition_not_arbitration")
        is True,
        "competition_not_arbitration",
        checks,
        failures,
    )
    _check(
        interaction.get("semantic_guards", {}).get(
            "temporary_occupation_not_structural_mutation"
        )
        is True,
        "temporary_occupation_not_structural_mutation",
        checks,
        failures,
    )
    _check(
        interaction.get("semantic_guards", {}).get(
            "historical_reactivation_not_new_truth"
        )
        is True,
        "historical_reactivation_not_new_truth",
        checks,
        failures,
    )

    _check(
        resource.get("resource_degradation_not_equal_knowledge_deletion") is True,
        "resource_degradation_not_deletion",
        checks,
        failures,
    )
    fixed_caps = resource.get("fixed_architecture_caps_forbidden", {})
    _check(
        all(
            fixed_caps.get(key) is True
            for key in (
                "max_nodes",
                "max_links",
                "max_depth",
                "fixed_retention_days",
                "fixed_activation_count",
                "fixed_carryover_count",
            )
        ),
        "no_fixed_architecture_resource_caps",
        checks,
        failures,
    )

    _check(
        subjective.get("subjective_policy", {}).get("subjective_strength_equals_truth")
        is False,
        "subjective_strength_not_truth",
        checks,
        failures,
    )
    _check(
        subjective.get("semantic_guards", {}).get("dormant_not_deleted") is True,
        "dormant_not_deleted",
        checks,
        failures,
    )
    _check(
        subjective.get("unknown_policy", {}).get("pcn_promote_unknown_to_fact")
        is False,
        "unknown_not_promoted_to_fact_by_pcn",
        checks,
        failures,
    )

    _check(
        handoff.get("handoff_type") == "CANDIDATE_ONLY",
        "pcn_to_intent_handoff_candidate_only",
        checks,
        failures,
    )
    _check(
        handoff.get("intent_implementation_started") is False,
        "no_intent_implementation",
        checks,
        failures,
    )
    _check(
        handoff.get("causal_implementation_started") is False,
        "no_causal_implementation",
        checks,
        failures,
    )
    _check(
        handoff.get("decision_action_implementation_started") is False,
        "no_decision_action_implementation",
        checks,
        failures,
    )

    clar_items = clar.get("clarifications", [])
    _check(len(clar_items) == 5, "five_clarifications_preserved", checks, failures)
    _check(
        all(item.get("closure_status") == "OPEN_DEFERRED" for item in clar_items),
        "no_forced_clarification_resolution",
        checks,
        failures,
    )
    _check(
        all(item.get("architecture_blocker") is False for item in clar_items),
        "clarifications_not_architecture_blockers",
        checks,
        failures,
    )

    _check(
        len(reuse.get("structural_blockers", [])) == 0,
        "no_structural_blockers",
        checks,
        failures,
    )

    _check(
        manifest.get("modified_existing_files") == [],
        "no_existing_asset_mutation",
        checks,
        failures,
    )
    _check(
        manifest.get("active_schema_changed") is False,
        "no_active_schema_change",
        checks,
        failures,
    )
    _check(
        manifest.get("active_contract_changed") is False,
        "no_active_contract_change",
        checks,
        failures,
    )
    _check(
        manifest.get("next_phase_auto_authorized") is False,
        "next_phase_not_auto_authorized_manifest",
        checks,
        failures,
    )

    _check(
        phase_contract.get("execution_mode") == "Planning Only",
        "planning_only_mode",
        checks,
        failures,
    )
    _check(
        phase_contract.get("next_phase_not_automatically_authorized") is True,
        "next_phase_not_auto_authorized_phase_contract",
        checks,
        failures,
    )
    _check(
        "python" in phase_contract.get("prohibited_agent_execution", []),
        "agent_python_execution_prohibited",
        checks,
        failures,
    )

    _emit(checks, failures)
    return 0 if not failures else 1


def _emit(checks: List[str], failures: List[str]) -> None:
    print("CHECKS")
    for item in checks:
        print(item)

    print("FAILED_CHECKS")
    for item in failures:
        print(item)

    print("PASSED_CHECK_COUNT")
    print(max(0, len(checks) - len(failures)))

    print("FAILED_CHECK_COUNT")
    print(len(failures))

    print("BLOCKER_COUNT")
    print(len(failures))

    print("FINAL_DECISION")
    print(
        "PCN_MODULE_CLOSURE_VERIFIED" if not failures else "BLOCKED_BY_VERIFIER_FAILURE"
    )

    print("NEXT")
    print(
        "WAIT_FOR_CHATGPT_V3_AUDIT"
        if not failures
        else "REMEDIATE_REPORTED_FAILURES_ONLY"
    )


if __name__ == "__main__":
    raise SystemExit(main())
