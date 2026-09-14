# -*- coding: utf-8 -*-
"""Document Surface — hybrid candidate policy v1."""

from __future__ import annotations

from typing import Any, Dict


def build_hybrid_candidate_policy() -> Dict[str, Any]:
    return {
        "policy_id": "document_surface_hybrid_candidate_policy_v1",
        "model_manager_route_selection": {
            "input": "case_profile_candidate",
            "output": "route_candidate",
            "not_execution_decision": True,
            "attention_gate_required": True,
        },
        "routes": {
            "option_a": {
                "role": "baseline_candidate",
                "when": ["single_flat_paper", "simple_clear_boundary", "abort_fallback", "uncertainty_baseline"],
            },
            "option_b": {
                "role": "segmentation_candidate_route",
                "when": ["overlap_separation_needed", "high_occlusion", "attached_surface_mask", "a_b_comparison"],
                "admission_required": True,
            },
        },
        "conflict_policy": {
            "on_a_b_conflict": "validation_review",
            "confidence_auto_override": False,
            "silent_fallback": False,
        },
        "relation_policy": {
            "attached_to_requires_evidence": True,
            "fake_relation_forbidden": True,
            "forced_multi_surface_forbidden": True,
        },
        "candidate_only": True,
        "not_fact": True,
    }
