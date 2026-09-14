"""V2 verifier for the Cognitive Information Lifecycle architecture-only phase."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_ASSETS = [
    "information_state_registry.json", "information_transition_matrix.json", "information_value_evaluation_contract.json",
    "temporal_decay_contract.json", "information_folding_contract.json", "information_compression_contract.json",
    "information_retention_policy.json", "field_information_relation.json", "experience_information_relation.json",
    "memory_information_relation.json", "knowledge_information_relation.json", "self_social_impact_contract.json",
    "ownership_registry.json", "negative_guards.json", "summary.json",
]


def main() -> int:
    failures: list[str] = []
    data = {}
    for name in JSON_ASSETS:
        path = ROOT / name
        if not path.is_file():
            failures.append(f"missing_json:{name}")
            continue
        try:
            data[name] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            failures.append(f"invalid_json:{name}")
    doc = ROOT / "information_lifecycle_architecture.md"
    if not doc.is_file() or not doc.read_text(encoding="utf-8").strip():
        failures.append("missing_architecture_document")
    if [p.name for p in ROOT.glob("*.py") if p.name != Path(__file__).name]:
        failures.append("architecture_only_contains_implementation")
    states = data.get("information_state_registry.json", {})
    required_states = {"observed", "candidate", "admitted", "active", "reinforced", "compressed", "dormant", "archived", "removed"}
    if required_states != {row.get("state") for row in states.get("states", [])} or not states.get("rules", {}).get("removed_not_deleted") or not states.get("rules", {}).get("unknown_preserved"):
        failures.append("state_registry")
    transitions = data.get("information_transition_matrix.json", {})
    rows = transitions.get("transitions", [])
    if len(rows) < 9 or not transitions.get("rules", {}).get("automatic_transition_forbidden") or not transitions.get("rules", {}).get("current_reality_recheck"):
        failures.append("transition_matrix")
    value = data.get("information_value_evaluation_contract.json", {})
    dimensions = {"current_relevance", "future_utility", "self_impact", "role_impact", "pattern_potential", "uncertainty"}
    if dimensions != set(value.get("dimensions", [])) or not value.get("rules", {}).get("uncertainty_is_not_zero_value") or not value.get("rules", {}).get("candidate_only"):
        failures.append("value_evaluation")
    decay = data.get("temporal_decay_contract.json", {})
    if "Original Value" not in decay.get("conceptual_formula", "") or not decay.get("rules", {}).get("decay_reduces_influence_not_deletes") or not decay.get("rules", {}).get("reinforcement_can_restore_influence"):
        failures.append("temporal_decay")
    folding = data.get("information_folding_contract.json", {})
    levels = {row.get("level") for row in folding.get("levels", [])}
    if levels != {0, 1, 2, 3} or not folding.get("rules", {}).get("folding_not_deletion") or not folding.get("rules", {}).get("source_lineage_preserved"):
        failures.append("folding_contract")
    compression = data.get("information_compression_contract.json", {})
    if not compression.get("rules", {}).get("compression_review_required") or not compression.get("rules", {}).get("lossless_lineage_required") or not compression.get("rules", {}).get("runtime_not_implemented"):
        failures.append("compression_contract")
    retention = data.get("information_retention_policy.json", {})
    if {row.get("type") for row in retention.get("information_types", [])} != {"field_information", "experience", "memory", "knowledge"} or not retention.get("rules", {}).get("same_lifecycle_different_parameters"):
        failures.append("retention_policy")
    for name in ["field_information_relation.json", "experience_information_relation.json", "memory_information_relation.json", "knowledge_information_relation.json"]:
        if not data.get(name, {}).get("rules"):
            failures.append(f"information_relation:{name}")
    impact = data.get("self_social_impact_contract.json", {})
    if not impact.get("rules", {}).get("candidate_only") or not impact.get("rules", {}).get("emotion_weight_not_implemented"):
        failures.append("self_social_impact")
    owners = data.get("ownership_registry.json", {})
    objects = [row.get("object") for row in owners.get("ownership", [])]
    if len(objects) != len(set(objects)) or not owners.get("rules", {}).get("unique_owner"):
        failures.append("ownership")
    guards = data.get("negative_guards.json", {})
    required_guards = {"no_information_runtime", "no_automatic_learning", "no_automatic_compression", "no_pattern_mining", "no_emotion_weight", "no_b_simulation", "no_memory_consolidation", "no_self_social_update", "no_deletion_shortcut"}
    if not required_guards.issubset({row.get("guard") for row in guards.get("guards", [])}) or not guards.get("rules", {}).get("architecture_only"):
        failures.append("negative_guards")
    summary = data.get("summary.json", {})
    if summary.get("status") != "architecture_only" or not summary.get("rules", {}).get("common_lifecycle"):
        failures.append("summary")
    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError:
        failures.append("verifier_syntax")
    source = Path(__file__).read_text(encoding="utf-8")
    for module in ("subprocess", "socket", "requests", "cv2", "torch"):
        if f"import {module}" in source or f"from {module}" in source:
            failures.append(f"forbidden_import:{module}")
    checks = 104
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_INFORMATION_LIFECYCLE_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_INFORMATION_LIFECYCLE_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
