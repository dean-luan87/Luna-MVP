# -*- coding: utf-8 -*-
"""Document Surface — controlled output policy v1."""

from __future__ import annotations

from typing import Any, Dict

CONTROLLED_OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_v1/"

OUTPUT_BOUNDARY_RULES = {
    "candidate_evidence_only": True,
    "no_fact_write": True,
    "no_production_registry_write": True,
    "no_model_manager_active_registry_modify": True,
    "no_training_data_write": True,
    "no_benchmark_canon_write": True,
    "trace_and_metrics_only": True,
}


def build_controlled_output_policy() -> Dict[str, Any]:
    return {
        "policy_id": "document_surface_controlled_output_policy_v1",
        "output_root": CONTROLLED_OUTPUT_ROOT,
        "boundary_rules": OUTPUT_BOUNDARY_RULES,
        "no_production_write": True,
        "no_runtime_registry_activation": True,
        "candidate_only": True,
        "not_fact": True,
    }
