from __future__ import annotations

from .corpus_v1 import build_golden_cognitive_case_categories_v1, build_empty_golden_corpus_manifest_v1
from .types_v1 import COGNITIVE_ASSERTION_KINDS, PERTURBATION_KINDS


def validate_golden_corpus_declaration_v1() -> dict:
    categories = build_golden_cognitive_case_categories_v1()
    errors = []
    if len(categories) != 16:
        errors.append(f"category_count:{len(categories)}")
    category_ids = [category.category_id for category in categories]
    if len(category_ids) != len(set(category_ids)):
        errors.append("duplicate_category_id")
    for category in categories:
        if not category.plane_a_assertion_kinds:
            errors.append(f"missing_plane_a_assertion:{category.category_id}")
        if any(assertion not in COGNITIVE_ASSERTION_KINDS for assertion in category.plane_a_assertion_kinds):
            errors.append(f"unknown_assertion:{category.category_id}")
        if any(perturbation not in PERTURBATION_KINDS for perturbation in category.allowed_perturbations):
            errors.append(f"unknown_perturbation:{category.category_id}")
    manifest = build_empty_golden_corpus_manifest_v1()
    if manifest["registered_dataset_refs"] or manifest["registered_sample_refs"]:
        errors.append("corpus_must_start_without_registered_data")
    if manifest["evaluation_only"] is not True or manifest["runtime_allowed"] is not False:
        errors.append("corpus_runtime_boundary_invalid")
    return {
        "phase": "Phase-P1-Luna-Level1-Field-Cognition-Golden-Corpus-And-Controlled-Evaluation-Suite-v1-001",
        "category_count": len(categories),
        "registered_dataset_count": len(manifest["registered_dataset_refs"]),
        "registered_sample_count": len(manifest["registered_sample_refs"]),
        "errors": errors,
        "all_checks_passed": not errors,
        "dataset_download": False,
        "model_invocation": False,
        "provider_invocation": False,
        "observation_execution": False,
        "runtime_allowed": False,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(validate_golden_corpus_declaration_v1(), indent=2))

