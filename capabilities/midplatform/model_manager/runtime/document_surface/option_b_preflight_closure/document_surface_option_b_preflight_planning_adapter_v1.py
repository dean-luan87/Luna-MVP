# -*- coding: utf-8 -*-
"""Document Surface — Option B preflight planning adapter (closure) v1."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_preflight_planning_adapter_v1 import (
    FINAL_BLOCKED as PLANNING_BLOCKED,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_preflight_planning_adapter_v1 import (
    FINAL_GO as PLANNING_GO,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_preflight_planning_adapter_v1 import (
    run_option_b_preflight_planning,
)

PLANNING_OUTPUTS = (
    "option_b_preflight_planning_summary.json",
    "option_b_preflight_candidate_scope.json",
    "option_b_dependency_availability_check_plan.json",
    "option_b_model_weight_presence_check_plan.json",
    "option_b_license_check_plan.json",
    "option_b_input_boundary_check_plan.json",
    "option_b_output_boundary_check_plan.json",
    "option_b_raw_output_normalization_check_plan.json",
    "option_b_candidate_schema_compliance_check_plan.json",
    "option_b_no_text_fact_leak_check_plan.json",
    "option_b_runtime_trace_check_plan.json",
    "option_b_preflight_abort_rollback_policy.json",
    "option_b_preflight_metrics_plan.json",
)


def run_preflight_planning_substage(
    *,
    repo_root: Path,
    out_dir: Path,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    result = run_option_b_preflight_planning(repo_root=repo_root, write_outputs=True)
    src = repo_root / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_planning_v1"
    checklist_src = repo_root / "capabilities/midplatform/model_manager/runtime/document_surface/option_b_preflight_planning/document_surface_option_b_preflight_checklist_schema_v1.json"
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        for name in PLANNING_OUTPUTS:
            if (src / name).is_file():
                shutil.copy2(src / name, out_dir / name)
        if checklist_src.is_file():
            (out_dir / "option_b_preflight_checklist_schema.json").write_text(
                checklist_src.read_text(encoding="utf-8"), encoding="utf-8"
            )
    decision = PLANNING_GO if result.get("final_decision") == PLANNING_GO else PLANNING_BLOCKED
    return {
        "substage": "preflight_planning",
        "preflight_planning_decision": decision,
        "passed": decision == PLANNING_GO,
        "result": result,
        "candidate_only": True,
        "not_fact": True,
    }
