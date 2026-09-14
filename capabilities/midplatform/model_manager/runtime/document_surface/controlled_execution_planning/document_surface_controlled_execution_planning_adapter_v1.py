# -*- coding: utf-8 -*-
"""Document Surface — controlled execution planning adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_execution_contract_v1 import (
    build_controlled_execution_trace_template,
    validate_controlled_contract_alignment,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_execution_smoke_plan_v1 import (
    build_controlled_smoke_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_input_registry_v1 import (
    build_controlled_input_registry_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_output_policy_v1 import (
    build_controlled_output_policy,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_cv2_dependency_admission_v1 import (
    CV2_IMPORTED_IN_PLANNING,
    build_cv2_dependency_admission_plan,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PLANNING_BLOCKED"
RECOMMENDED_NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Preflight-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"


def _load_abort_policy(repo_root: Path) -> Dict[str, Any]:
    path = repo_root / "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_planning/document_surface_abort_condition_policy_v1.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _load_rollback_policy(repo_root: Path) -> Dict[str, Any]:
    path = repo_root / "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_planning/document_surface_rollback_policy_v1.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _load_trace_schema(repo_root: Path) -> Dict[str, Any]:
    path = repo_root / "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_planning/document_surface_runtime_trace_schema_v1.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def run_controlled_execution_planning(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    cv2_admission = build_cv2_dependency_admission_plan()
    input_reg = build_controlled_input_registry_plan()
    output_pol = build_controlled_output_policy()
    contract_align = validate_controlled_contract_alignment()
    trace_template = build_controlled_execution_trace_template()
    smoke_plan = build_controlled_smoke_plan()
    abort_pol = _load_abort_policy(root)
    rollback_pol = _load_rollback_policy(root)
    trace_schema = _load_trace_schema(root)

    abort_count = len(abort_pol.get("abort_conditions") or [])
    trace_required = trace_schema.get("required") or []

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Planning-v1-001",
        "runtime_id": "document_surface_detector_v1",
        "implementation_mode": "option_a_classical_cv_boundary",
        "controlled_execution_planning_only": True,
        "real_execution_enabled": False,
        "cv2_dependency_not_admitted": cv2_admission.get("cv2_dependency_not_admitted") is True,
        "cv2_imported_in_planning": CV2_IMPORTED_IN_PLANNING,
        "input_registry_defined": input_reg.get("image_count", 0) >= 6,
        "abort_condition_count": abort_count,
        "controlled_smoke_cases": smoke_plan.get("case_count"),
        "protocol_compliance_check": "required",
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "recommended_next_phase": RECOMMENDED_NEXT_PHASE,
        "parallel_next_track": PARALLEL_NEXT_TRACK,
        "candidate_only": True,
        "not_fact": True,
        "planned_at": datetime.now(timezone.utc).isoformat(),
    }

    out_dir = root / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_planning_v1"
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "controlled_execution_planning_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "cv2_dependency_admission_plan.json").write_text(json.dumps(cv2_admission, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_input_registry_plan.json").write_text(json.dumps(input_reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_output_policy_summary.json").write_text(json.dumps(output_pol, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "runtime_trace_schema_summary.json").write_text(json.dumps({"schema": trace_schema, "template": trace_template, "required_fields_complete": all(f in trace_template for f in trace_required)}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "abort_condition_policy_summary.json").write_text(json.dumps(abort_pol, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "rollback_policy_summary.json").write_text(json.dumps(rollback_pol, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "controlled_smoke_plan_summary.json").write_text(json.dumps(smoke_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "cv2_admission": cv2_admission,
        "input_registry": input_reg,
        "output_policy": output_pol,
        "contract_alignment": contract_align,
        "trace_template": trace_template,
        "smoke_plan": smoke_plan,
        "abort_policy": abort_pol,
        "rollback_policy": rollback_pol,
    }
