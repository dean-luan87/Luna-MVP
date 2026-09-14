"""V0 static contract verifier for Self–World Boundary Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "self_boundary_schema.json", "identity_boundary_contract.json",
    "capability_boundary_contract.json", "ownership_boundary_contract.json",
    "self_memory_boundary.json", "social_self_boundary.json",
    "field_memory_boundary.json", "self_evolution_contract.json",
    "self_growth_governance.json", "ownership_registry.json",
    "dependency_boundary.json", "negative_guards.json", "summary.json",
]
MD_FILES = [
    "self_world_boundary_architecture.md", "self_identity_boundary_model.md",
    "self_evolution_boundary_model.md", "memory_self_boundary_model.md",
    "implementation_plan.md",
]
VERIFIER = "verify_self_world_boundary_architecture_v1.py"


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main() -> int:
    checks = 0
    failed: list[str] = []

    def check(condition: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failed.append(label)

    files = {p.name for p in ROOT.iterdir() if p.is_file()}
    check(set(JSON_FILES) | set(MD_FILES) | {VERIFIER} <= files, "required_assets")
    check({p.name for p in ROOT.glob("*.py")} == {VERIFIER}, "no_runtime_python")
    assets: dict[str, dict] = {}
    for name in JSON_FILES:
        try:
            assets[name] = load(name)
            check(isinstance(assets[name], dict), f"json_object:{name}")
        except (OSError, json.JSONDecodeError):
            check(False, f"json_parse:{name}")
    for name in MD_FILES:
        try:
            check((ROOT / name).read_text(encoding="utf-8").strip() != "", f"markdown_nonempty:{name}")
        except OSError:
            check(False, f"markdown_read:{name}")
    try:
        ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        check(True, "verifier_ast")
    except (OSError, SyntaxError):
        check(False, "verifier_ast")

    schema = assets["self_boundary_schema.json"]
    required_fields = {"boundary_id", "external_world_ref", "internal_state_refs", "identity_ref", "capability_refs", "constitution_ref", "boundary_types", "ownership_context", "provenance", "unknowns"}
    check(required_fields <= set(schema["required"]), "boundary_fields")
    boundaries = ["Physical Boundary", "Computational Boundary", "Cognitive Boundary", "Identity Boundary", "Ownership Boundary"]
    check(schema["boundary_types"] == boundaries and schema["reality_is_external_authority"] is True and schema["self_is_not_all_memory"] is True and schema["social_self_is_not_self"] is True and schema["candidate_only"] is True and schema["identity_mutation"] is False and schema["self_runtime"] is False, "boundary_schema")

    identity = assets["identity_boundary_contract.json"]
    protected = {"Constitution", "Core Identity", "Safety Boundary"}
    check(set(identity["protected_from_automatic_change"]) == protected and identity["memory_direct_identity_change"] is False and identity["experience_direct_identity_change"] is False and identity["social_feedback_replace_self"] is False and identity["capability_failure_destroy_identity"] is False and identity["emotion_identity_rewrite"] is False, "identity_protection")
    check(identity["candidate_only"] is True and identity["self_governance_required"] is True, "identity_boundary")

    capability = assets["capability_boundary_contract.json"]
    check(set(capability["boundary_types"]) == {"Physical Boundary", "Computational Boundary", "Cognitive Boundary"}, "capability_boundary_types")
    check(set(capability["capability_claim_requires"]) == {"Capability Evidence", "Context Scope", "Confidence", "Limitation", "Unknowns"}, "capability_claim_context")
    check(capability["capability_is_context_scoped"] is True and capability["capability_does_not_imply_universal_ability"] is True and capability["failure_updates_capability_evidence"] is True and capability["failure_does_not_update_identity"] is True and capability["capability_governance_is_external_owner"] is True and capability["automatic_capability_change"] is False and capability["model_output_is_not_capability_fact"] is True, "capability_boundary")

    ownership_boundary = assets["ownership_boundary_contract.json"]
    check(set(ownership_boundary["ownership_domains"]) == {"Luna Self State", "Luna Capability State", "User Data", "Other Person Data", "Field State", "External Reality", "Knowledge Source"}, "ownership_domains")
    check(len(ownership_boundary["rules"]) == 6 and ownership_boundary["ownership_requires_provenance"] is True and ownership_boundary["cross_boundary_copy_requires_candidate"] is True and ownership_boundary["cross_boundary_copy_is_not_automatic"] is True and ownership_boundary["privacy_boundary_preserved"] is True, "ownership_boundary")

    self_memory = assets["self_memory_boundary.json"]
    check(self_memory["memory_types"] == ["Self Memory", "Social Memory", "Field Memory"], "memory_types")
    check(self_memory["social_memory_is_not_self_memory"] is True and self_memory["field_memory_is_not_self_memory"] is True and self_memory["memory_is_not_identity"] is True and self_memory["memory_direct_identity_change"] is False and self_memory["memory_overrides_reality"] is False and self_memory["current_reality_precedence"] is True and self_memory["retrieval_is_contextual"] is True and self_memory["candidate_only"] is True, "memory_boundary")

    social = assets["social_self_boundary.json"]
    check(social["social_self_is_not_self"] is True and set(social["allowed_self_interface"]) == {"read_self_context", "request_self_context", "submit_growth_candidate"}, "social_interface")
    check(set(social["forbidden_self_interface"]) == {"replace_self", "rewrite_identity", "modify_constitution", "rewrite_safety_boundary"} and social["social_feedback_replace_self"] is False and social["social_runtime"] is False and social["candidate_only"] is True, "social_boundary")

    field_memory = assets["field_memory_boundary.json"]
    check(field_memory["field_memory_is_not_self"] is True and field_memory["field_memory_is_not_reality"] is True and field_memory["field_memory_does_not_modify_identity"] is True and field_memory["field_memory_does_not_override_current_field"] is True and field_memory["current_field_precedence"] is True and field_memory["candidate_only"] is True, "field_memory_boundary")

    evolution = assets["self_evolution_contract.json"]
    check(evolution["flow"] == ["Experience", "Memory", "Schema", "Growth Candidate", "Self Review", "Self Evolution Candidate"], "evolution_flow")
    check(set(evolution["mutable_candidates"]) == {"Capability", "Strategy", "Schema", "Capability Confidence"} and set(evolution["protected_boundaries"]) == {"Constitution", "Identity", "Safety Boundary"}, "evolution_scope")
    check(evolution["automatic_self_modification"] is False and evolution["direct_identity_change"] is False and evolution["direct_constitution_change"] is False and evolution["direct_safety_change"] is False and evolution["self_review_required"] is True and evolution["candidate_only"] is True, "evolution_boundary")

    growth = assets["self_growth_governance.json"]
    check(growth["owner"] == "Self Layer" and set(growth["review_criteria"]) == {"Evidence Quality", "Repetition or Impact", "Capability Relevance", "Stability", "Reversibility", "Constitution Compliance", "Identity Boundary"}, "growth_owner")
    check(set(growth["outputs"]) == {"Approved Growth Candidate", "Rejected Growth Candidate", "Deferred Growth Candidate", "Self Evolution Candidate"} and growth["single_outcome_is_insufficient"] is True and growth["self_governance_required"] is True and growth["automatic_update"] is False and growth["candidate_only"] is True, "growth_boundary")

    ownership = assets["ownership_registry.json"]
    owners = [x["owner"] for x in ownership["ownership"]]
    required_owners = {"Self Layer", "Social Self", "Memory", "Schema", "Capability Governance", "Constitution", "Field", "Integration", "Self Evolution", "Knowledge", "Action Boundary"}
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)), "unique_owners")
    check(required_owners <= set(owners), "ownership_coverage")
    check(all(x.get("writer") and x.get("reader") for x in ownership["ownership"]), "ownership_writer_reader")

    dependency = assets["dependency_boundary.json"]
    required_forbidden = {"Memory -> Direct Identity Change", "Experience -> Direct Self Modification", "Social Feedback -> Replace Self", "Capability Failure -> Destroy Identity", "Knowledge -> Rewrite Constitution", "Social Self -> Rewrite Identity", "Field Memory -> Modify Self Identity", "Capability Output -> Replace Reality", "Emotion -> Rewrite Identity", "Outcome -> Direct Identity Change"}
    check(required_forbidden <= set(dependency["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency["no_self_runtime"] is True and dependency["no_identity_mutation"] is True and dependency["no_automatic_personality_change"] is True and dependency["no_emotion_runtime"] is True and dependency["no_social_runtime"] is True and dependency["no_learning_runtime"] is True and dependency["reality_is_external_authority"] is True and dependency["social_self_is_not_self"] is True, "dependency_boundary")

    guards = assets["negative_guards.json"]
    required_guards = {"memory_direct_identity_change", "experience_direct_self_modification", "social_feedback_replace_self", "capability_failure_destroy_identity", "knowledge_rewrite_constitution", "self_runtime", "identity_modification", "automatic_personality_change", "emotion_runtime", "social_runtime", "learning_runtime", "memory_override_reality", "field_memory_replace_self", "capability_output_replace_reality", "outcome_direct_identity_change", "schema_modify_constitution", "provider_modify_self", "runtime_rewrite_boundary", "model_calls", "hardware_control", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(guards["reality_is_external_authority"] is True and guards["self_is_not_all_memory"] is True and guards["social_self_is_not_self"] is True and guards["identity_continuity"] is True and guards["capability_is_context_scoped"] is True and guards["growth_candidate_only"] is True and guards["unknowns_preserved"] is True, "negative_invariants")

    summary = assets["summary.json"]
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_SELF_WORLD_BOUNDARY_ARCHITECTURE_READY", "summary_status")
    check(summary["boundary_types"] == boundaries and summary["memory_types"] == ["Self Memory", "Social Memory", "Field Memory"], "summary_boundaries")
    check(summary["self_evolution_flow"] == ["Experience", "Memory", "Schema", "Growth Candidate", "Self Review", "Self Evolution Candidate"], "summary_evolution")
    check(summary["runtime"] is False and summary["self_runtime"] is False and summary["identity_modification"] is False and summary["automatic_personality_change"] is False and summary["emotion_runtime"] is False and summary["social_runtime"] is False and summary["learning_runtime"] is False, "summary_boundary")
    check(len(summary["reusable_assets"]) >= 7 and len(summary["parallel_risks"]) >= 3 and len(summary["migration_mapping"]) >= 3, "summary_inventory")

    forbidden_imports = {"subprocess", "socket", "requests", "cv2", "torch", "transformers", "sqlite3", "psycopg2"}
    try:
        tree = ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        imports = {n.names[0].name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) and n.names}
        imports |= {n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
        check(not imports & forbidden_imports, "verifier_no_runtime_imports")
    except (OSError, SyntaxError):
        check(False, "verifier_no_runtime_imports")

    blockers = len(failed)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {checks - blockers}")
    print(f"FAILED_CHECK_COUNT: {blockers}")
    print(f"BLOCKER_COUNT: {blockers}")
    if blockers:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_SELF_WORLD_BOUNDARY_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_SELF_WORLD_BOUNDARY_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
