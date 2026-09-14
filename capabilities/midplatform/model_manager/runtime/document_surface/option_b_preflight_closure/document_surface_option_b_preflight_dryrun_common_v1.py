# -*- coding: utf-8 -*-
"""Document Surface — Option B preflight closure dryrun helpers v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PREFLIGHT_IDS = frozenset({
    "family_a_classical_helper_ok_candidate",
    "family_c_document_specific_surface_model_ok_for_preflight",
})

ABORT_ROLLBACK = {
    "no_active_registry_update": True,
    "no_runtime_activation": True,
    "no_silent_fallback_to_option_a": True,
    "no_fallback_to_ocr_vlm_layout": True,
    "retain_trace": True,
    "rollback_action": "retain_trace_return_to_preflight_planning",
}


def load_fixture_registry(root: Path) -> Dict[str, Any]:
    p = root / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_v1/option_b_candidate_fixture_registry.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def get_preflight_fixtures(root: Path) -> List[Dict[str, Any]]:
    reg = load_fixture_registry(root)
    return [f for f in (reg.get("fixtures") or []) if f.get("model_candidate_id") in PREFLIGHT_IDS]


def base_trace(*, candidate_id: str, run_id: str) -> Dict[str, Any]:
    return {
        "preflight_run_id": run_id,
        "candidate_id": candidate_id,
        "protocol_refs": [
            "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1",
            "Runtime Boundary Contract",
            "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1",
        ],
        "execution_performed": False,
        "segmentation_performed": False,
        "active_model_selected": False,
        "active_registry_updated": False,
        "candidate_only": True,
        "not_fact": True,
    }
