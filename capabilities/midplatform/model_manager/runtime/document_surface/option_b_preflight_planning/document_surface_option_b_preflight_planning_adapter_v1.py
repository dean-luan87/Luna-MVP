# -*- coding: utf-8 -*-
"""Document Surface — Option B preflight planning adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_candidate_schema_compliance_check_plan_v1 import (
    build_candidate_schema_compliance_check_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_dependency_availability_check_plan_v1 import (
    build_dependency_availability_check_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_input_boundary_check_plan_v1 import (
    build_input_boundary_check_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_license_check_plan_v1 import (
    build_license_check_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_model_weight_presence_check_plan_v1 import (
    build_model_weight_presence_check_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_no_text_fact_leak_check_plan_v1 import (
    build_no_text_fact_leak_check_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_output_boundary_check_plan_v1 import (
    build_output_boundary_check_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_preflight_candidate_scope_v1 import (
    build_preflight_candidate_scope,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_preflight_metrics_plan_v1 import (
    build_preflight_metrics_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_raw_output_normalization_check_plan_v1 import (
    build_raw_output_normalization_check_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_runtime_trace_check_plan_v1 import (
    build_runtime_trace_check_plan,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_PREFLIGHT_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_PREFLIGHT_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Preflight-Closure-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_preflight_planning_v1"
PLAN_DIR = "capabilities/midplatform/model_manager/runtime/document_surface/option_b_preflight_planning"

ALIGNMENT_POST_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_POST_REVIEW_GO"
ALIGNMENT_POST_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_post_review_v1/"
    "option_b_protocol_alignment_post_review_summary.json"
)


def _load_json(root: Path, rel: str) -> Dict[str, Any]:
    p = root / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def run_option_b_preflight_planning(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    blockers: List[str] = []

    alignment_post = _load_json(root, ALIGNMENT_POST_REL)
    if alignment_post.get("final_decision") != ALIGNMENT_POST_GO:
        blockers.append(f"upstream.alignment_post_review.not_go={alignment_post.get('final_decision')}")
    if alignment_post.get("preflight_planning_allowed") is not True:
        blockers.append("upstream.preflight_planning_not_allowed")
    if entry.get("option_b_model_skill_admission_protocol_alignment_post_review_ready") is not True:
        blockers.append("registry.alignment_post_review_ready")

    scope = build_preflight_candidate_scope()
    dep = build_dependency_availability_check_plan()
    weight = build_model_weight_presence_check_plan()
    license_plan = build_license_check_plan()
    input_plan = build_input_boundary_check_plan()
    output_plan = build_output_boundary_check_plan()
    norm = build_raw_output_normalization_check_plan()
    schema = build_candidate_schema_compliance_check_plan()
    leak = build_no_text_fact_leak_check_plan()
    trace = build_runtime_trace_check_plan()
    abort_policy = _load_json(root, f"{PLAN_DIR}/document_surface_option_b_preflight_abort_rollback_policy_v1.json")
    metrics = build_preflight_metrics_plan(scope=scope, abort_policy=abort_policy)

    if scope.get("preflight_candidate_count") != 2:
        blockers.append("scope.preflight_count")
    if dep.get("install_allowed") is not False or dep.get("download_allowed") is not False:
        blockers.append("dep.install_download")
    if input_plan.get("image_read_allowed") is not False:
        blockers.append("input.image_read")
    if output_plan.get("active_registry_update_allowed") is not False:
        blockers.append("output.active_registry")
    if len(abort_policy.get("abort_conditions") or []) < 16:
        blockers.append("abort.incomplete")
    if len(trace.get("required_trace_fields") or []) < 16:
        blockers.append("trace.incomplete")
    if len(schema.get("allowed_output_types") or []) < 6:
        blockers.append("schema.allowed")

    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Preflight-Planning-v1-001",
        "preflight_planning_only": True,
        "preflight_execution_forbidden": True,
        "segmentation_execution_forbidden": True,
        "model_download_forbidden": True,
        "dependency_install_forbidden": True,
        "image_read_forbidden": True,
        "runtime_activation_allowed": False,
        "controlled_execution_allowed": False,
        "option_b_execution_allowed": False,
        "boundary_status": "frozen",
        "preflight_planning_completed": decision == FINAL_GO,
        "preflight_execution_allowed": False,
        "active_model_selected": False,
        "active_skill_selected": False,
        "active_registry_update_allowed": False,
        "protocol_compliance_check": "required",
        "protocol_compliance_passed": True,
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "primary_contract": "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1",
        "referenced_protocols": [
            "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1",
            "Runtime Boundary Contract",
            "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1",
            "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1",
            "Change Control / Review / Freeze",
        ],
        "metrics_plan": metrics,
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "recommended_next_phase": NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL if decision == FINAL_GO else None,
        "final_decision": decision,
        "planned_at": datetime.now(timezone.utc).isoformat(),
        "candidate_only": True,
        "not_fact": True,
    }

    out_dir = root / OUTPUT_ROOT
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "option_b_preflight_planning_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_preflight_candidate_scope.json").write_text(json.dumps(scope, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_dependency_availability_check_plan.json").write_text(json.dumps(dep, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_model_weight_presence_check_plan.json").write_text(json.dumps(weight, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_license_check_plan.json").write_text(json.dumps(license_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_input_boundary_check_plan.json").write_text(json.dumps(input_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_output_boundary_check_plan.json").write_text(json.dumps(output_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_raw_output_normalization_check_plan.json").write_text(json.dumps(norm, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_candidate_schema_compliance_check_plan.json").write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_no_text_fact_leak_check_plan.json").write_text(json.dumps(leak, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_runtime_trace_check_plan.json").write_text(json.dumps(trace, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_preflight_abort_rollback_policy.json").write_text(json.dumps(abort_policy, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_preflight_metrics_plan.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "scope": scope,
        "dependency_plan": dep,
        "weight_plan": weight,
        "license_plan": license_plan,
        "input_plan": input_plan,
        "output_plan": output_plan,
        "normalization_plan": norm,
        "schema_plan": schema,
        "leak_plan": leak,
        "trace_plan": trace,
        "abort_policy": abort_policy,
    }
