from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .types_v1 import COGNITIVE_ASSERTION_KINDS, PERTURBATION_KINDS


@dataclass(frozen=True)
class GoldenCognitiveCaseCategoryV1:
    category_id: str
    cognitive_property: str
    world_ground_truth_characteristics: Tuple[str, ...]
    allowed_perturbations: Tuple[str, ...]
    plane_a_assertion_kinds: Tuple[str, ...]
    plane_b_observations: Tuple[str, ...]
    failure_attribution_rules: Tuple[str, ...]


GOLDEN_CORPUS_ID = "luna-level1-field-cognition-golden-corpus"
GOLDEN_CORPUS_VERSION = "v1"


def build_golden_cognitive_case_categories_v1() -> Tuple[GoldenCognitiveCaseCategoryV1, ...]:
    categories = (
        ("obvious_field", "minimum sufficient single-cycle cognition", ("target_exists", "visible"), ("baseline",), ("MUST_STOP_WHEN_MINIMUM_SUFFICIENT_INFORMATION_EXISTS", "MUST_PRESERVE_OWNER_BOUNDARIES"), ("evidence_usefulness", "latency"), ("wrong stop or owner => LUNA_COGNITIVE",)),
        ("multiple_candidate_field", "candidate disambiguation", ("multiple_candidates", "ambiguous_relation"), ("baseline", "distractor_similarity"), ("MUST_PRESERVE_UNCERTAINTY", "MUST_FORM_INFORMATION_GAP_WHEN_REQUIRED"), ("candidate_stability", "conflict_rate"), ("bad ambiguity handling => LUNA_COGNITIVE",)),
        ("irrelevant_distractors", "ignore irrelevant evidence", ("target_exists", "irrelevant_objects"), ("irrelevant_clutter", "distractor_similarity"), ("MUST_PRESERVE_OWNER_BOUNDARIES",), ("false_evidence_rate", "evidence_usefulness"), ("misclassification source unresolved until traced",)),
        ("target_absent", "represent absence without forced success", ("target_absent",), ("baseline", "irrelevant_clutter"), ("MUST_PRESERVE_UNCERTAINTY", "MUST_NOT_PROMOTE_PROVIDER_OUTPUT_TO_WORLD_TRUTH"), ("false_positive_rate",), ("provider false positive => EXTERNAL_CAPABILITY; misuse => LUNA_COGNITIVE",)),
        ("missing_critical_information", "detect missing evidence", ("target_exists", "required_fact_not_visible"), ("missing_evidence", "partial_occlusion"), ("MUST_FORM_INFORMATION_GAP_WHEN_REQUIRED", "MUST_NOT_DECLARE_SUFFICIENT_WITH_REQUIRED_INFORMATION_MISSING"), ("missing_evidence_rate",), ("missing handling => LUNA_COGNITIVE",)),
        ("partial_occlusion", "preserve visibility limits", ("target_exists", "partially_visible"), ("partial_occlusion", "viewpoint_variation"), ("MUST_PRESERVE_UNCERTAINTY", "MUST_REOBSERVE_WHEN_REQUIRED"), ("visible_vs_occluded_quality",), ("provider miss vs planning error must be separated",)),
        ("conflicting_evidence", "retain and resolve conflict", ("conflicting_observations",), ("conflicting_evidence", "duplicate_evidence"), ("MUST_PRESERVE_UNCERTAINTY", "MUST_NOT_DECLARE_SUFFICIENT_WITH_REQUIRED_INFORMATION_MISSING"), ("conflict_rate", "stability"), ("conflict ignored => LUNA_COGNITIVE",)),
        ("false_external_evidence", "reject incorrect provider candidate", ("target_exists", "provider_false_candidate"), ("false_evidence",), ("MUST_NOT_PROMOTE_PROVIDER_OUTPUT_TO_WORLD_TRUTH", "MUST_PRESERVE_UNCERTAINTY"), ("false_evidence_rate",), ("source result => EXTERNAL_CAPABILITY; misuse => LUNA_COGNITIVE",)),
        ("stale_evidence", "invalidate stale observation", ("temporal_validity", "source_change"), ("stale_evidence", "delayed_evidence"), ("MUST_NOT_DECLARE_SUFFICIENT_WITH_REQUIRED_INFORMATION_MISSING", "MUST_FORM_INFORMATION_GAP_WHEN_REQUIRED"), ("stale_result_rate",), ("stale handling => LUNA_COGNITIVE or PROVIDER by detector",)),
        ("wrong_attention_trap", "select useful observation target", ("target_exists", "distractor_region"), ("wrong_attention", "irrelevant_clutter"), ("MUST_FORM_INFORMATION_GAP_WHEN_REQUIRED", "MUST_PRESERVE_OWNER_BOUNDARIES"), ("attention_support",), ("wrong target choice => LUNA_COGNITIVE",)),
        ("capability_mismatch", "recognize unsuitable capability", ("required_modality", "capability_mismatch"), ("capability_unavailable",), ("MUST_FORM_INFORMATION_GAP_WHEN_REQUIRED", "MUST_REOBSERVE_WHEN_REQUIRED"), ("capability_fitness",), ("resolution => governance; misuse => LUNA_COGNITIVE",)),
        ("reobservation_required", "target next observation at gap", ("first_view_incomplete", "followup_resolves_gap"), ("missing_evidence", "observation_budget_restriction"), ("MUST_REOBSERVE_WHEN_REQUIRED", "MUST_NOT_REOBSERVE_WITHOUT_JUSTIFICATION"), ("cycle_burden", "evidence_stability"), ("bad target/loop => LUNA_COGNITIVE",)),
        ("hypothesis_revision", "revise candidate with new evidence", ("initial_hypothesis", "later_disambiguating_fact"), ("delayed_evidence", "viewpoint_variation"), ("MUST_PRESERVE_UNCERTAINTY", "MUST_PRESERVE_OWNER_BOUNDARIES"), ("revision_support",), ("revision error => LUNA_COGNITIVE",)),
        ("premature_sufficiency_trap", "avoid early sufficiency", ("required_fact_missing", "plausible_partial_evidence"), ("missing_evidence", "false_evidence"), ("MUST_NOT_DECLARE_SUFFICIENT_WITH_REQUIRED_INFORMATION_MISSING", "MUST_FORM_INFORMATION_GAP_WHEN_REQUIRED"), ("confidence_not_sufficiency",), ("premature status => LUNA_COGNITIVE",)),
        ("stop_condition_test", "stop at minimum sufficient cognition", ("minimum_facts_visible", "no_unresolved_required_gap"), ("baseline", "observation_budget_restriction"), ("MUST_STOP_WHEN_MINIMUM_SUFFICIENT_INFORMATION_EXISTS", "MUST_NOT_REOBSERVE_WITHOUT_JUSTIFICATION"), ("unnecessary_cycle_count",), ("failure to stop => LUNA_COGNITIVE",)),
        ("environment_state_change", "track changed world between cycles", ("state_before", "state_after"), ("delayed_evidence", "lighting_variation", "viewpoint_variation"), ("MUST_PRESERVE_UNCERTAINTY", "MUST_FORM_INFORMATION_GAP_WHEN_REQUIRED"), ("temporal_stability", "change_detection"), ("source change vs cognition handling traced separately",)),
    )
    return tuple(
        GoldenCognitiveCaseCategoryV1(
            category_id=category_id,
            cognitive_property=property_text,
            world_ground_truth_characteristics=world_gt,
            allowed_perturbations=perturbations,
            plane_a_assertion_kinds=assertions,
            plane_b_observations=plane_b,
            failure_attribution_rules=rules,
        )
        for category_id, property_text, world_gt, perturbations, assertions, plane_b, rules in categories
    )


def build_empty_golden_corpus_manifest_v1() -> dict:
    return {
        "corpus_id": GOLDEN_CORPUS_ID,
        "corpus_version": GOLDEN_CORPUS_VERSION,
        "owner": "Evaluation Governance",
        "purpose": "Luna Field Cognition Level-1 evaluation",
        "dataset_registry_ref": "luna-evaluation-world-observation-corpus-registry:v1",
        "registration_status": "CATEGORIES_DECLARED_NO_DATASET_REGISTERED",
        "categories": [
            {
                "category_id": category.category_id,
                "cognitive_property": category.cognitive_property,
                "world_ground_truth_characteristics": list(category.world_ground_truth_characteristics),
                "allowed_perturbations": list(category.allowed_perturbations),
                "plane_a_assertions": list(category.plane_a_assertion_kinds),
                "plane_b_observations": list(category.plane_b_observations),
                "failure_attribution_rules": list(category.failure_attribution_rules),
            }
            for category in build_golden_cognitive_case_categories_v1()
        ],
        "registered_dataset_refs": [],
        "registered_sample_refs": [],
        "evaluation_only": True,
        "runtime_allowed": False,
    }

