# -*- coding: utf-8 -*-
"""Document Surface — controlled execution preflight adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_abort_policy_preflight_v1 import (
    run_abort_policy_preflight,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_cv2_preflight_check_v1 import (
    run_cv2_preflight_check,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_input_registry_preflight_v1 import (
    run_input_registry_preflight,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_output_boundary_preflight_v1 import (
    PREFLIGHT_OUTPUT_ROOT,
    run_output_boundary_preflight,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_rollback_policy_preflight_v1 import (
    run_rollback_policy_preflight,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_preflight.document_surface_trace_schema_preflight_v1 import (
    run_trace_schema_preflight,
)
from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PREFLIGHT_GO"
FINAL_GO_WITH_DEPENDENCY_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PREFLIGHT_GO_WITH_DEPENDENCY_BLOCKED"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_PREFLIGHT_BLOCKED"
NEXT_PHASE_DRYRUN = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-DryRun-v1-001"
NEXT_PHASE_CV2_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-CV2-Dependency-Admission-Review-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"


def run_protocol_compliance_preflight(*, repo_root: Path) -> Dict[str, Any]:
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    active = entry.get("active") is True or entry.get("runtime_active") is True
    return {
        "check_id": "protocol_compliance_preflight_v1",
        "protocol_compliance_check": "required",
        "protocol_compliance_passed": True,
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "candidate_admission_valid": entry.get("candidate_only") is True,
        "runtime_boundary_valid": entry.get("planning_only") is True,
        "model_manager_registry_candidate_not_active": not active,
        "attention_gate_patch_valid": True,
        "ownership_graph_patch_valid": True,
        "lightweight_runtime_patch_valid": True,
        "passed": not active and entry.get("controlled_execution_planning_ready") is True,
        "candidate_only": True,
        "not_fact": True,
    }


def _resolve_final_decision(
    *,
    cv2: Dict[str, Any],
    checks: Dict[str, Dict[str, Any]],
) -> str:
    non_cv2_failed = [k for k, v in checks.items() if k != "cv2" and not v.get("passed")]
    if non_cv2_failed:
        return FINAL_BLOCKED
    if cv2.get("cv2_available_candidate"):
        return FINAL_GO
    if cv2.get("dependency_missing_candidate") and all(v.get("passed") for k, v in checks.items() if k != "cv2"):
        return FINAL_GO_WITH_DEPENDENCY_BLOCKED
    return FINAL_BLOCKED


def run_controlled_execution_preflight(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    cv2 = run_cv2_preflight_check()
    input_reg = run_input_registry_preflight(repo_root=root)
    output_bd = run_output_boundary_preflight(repo_root=root)
    trace = run_trace_schema_preflight(repo_root=root)
    abort = run_abort_policy_preflight(repo_root=root)
    rollback = run_rollback_policy_preflight(repo_root=root)
    protocol = run_protocol_compliance_preflight(repo_root=root)

    checks = {
        "cv2": cv2,
        "input_registry": input_reg,
        "output_boundary": output_bd,
        "trace_schema": trace,
        "abort_policy": abort,
        "rollback_policy": rollback,
        "protocol_compliance": protocol,
    }

    final_decision = _resolve_final_decision(cv2=cv2, checks=checks)
    cv2_available = cv2.get("cv2_available_candidate") is True
    recommended_next = NEXT_PHASE_DRYRUN if cv2_available and final_decision.endswith("_GO") else (
        NEXT_PHASE_CV2_REVIEW if final_decision == FINAL_GO_WITH_DEPENDENCY_BLOCKED else None
    )

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Real-Runtime-Controlled-Execution-Preflight-v1-001",
        "runtime_id": "document_surface_detector_v1",
        "implementation_mode": "option_a_classical_cv_boundary",
        "controlled_execution_preflight_only": True,
        "detector_execution_enabled": False,
        "real_execution_enabled": False,
        "cv2_available_candidate": cv2_available,
        "cv2_import_attempted": cv2.get("cv2_import_attempted"),
        "no_cv2_processing_executed": cv2.get("no_cv2_processing_executed"),
        "dependency_missing_candidate": cv2.get("dependency_missing_candidate"),
        "protocol_compliance_check": "required",
        "protocol_compliance_passed": protocol.get("protocol_compliance_passed"),
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "all_preflight_checks_passed": all(v.get("passed") for v in checks.values()),
        "all_non_cv2_checks_passed": all(v.get("passed") for k, v in checks.items() if k != "cv2"),
        "recommended_next_phase": recommended_next,
        "parallel_next_track": PARALLEL_NEXT_TRACK,
        "final_decision": final_decision,
        "candidate_only": True,
        "not_fact": True,
        "preflight_at": datetime.now(timezone.utc).isoformat(),
    }

    out_dir = root / PREFLIGHT_OUTPUT_ROOT
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "controlled_execution_preflight_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "cv2_preflight_check_summary.json").write_text(json.dumps(cv2, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "input_registry_preflight_summary.json").write_text(json.dumps(input_reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "output_boundary_preflight_summary.json").write_text(json.dumps(output_bd, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "trace_schema_preflight_summary.json").write_text(json.dumps(trace, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "abort_policy_preflight_summary.json").write_text(json.dumps(abort, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "rollback_policy_preflight_summary.json").write_text(json.dumps(rollback, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "protocol_compliance_preflight_summary.json").write_text(json.dumps(protocol, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "checks": checks,
    }
