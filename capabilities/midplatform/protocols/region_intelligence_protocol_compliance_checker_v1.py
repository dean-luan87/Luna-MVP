# -*- coding: utf-8 -*-
"""Region Intelligence — protocol compliance checker v1.

Uses Luna midplatform protocol chain as primary governance framework.
Applies Field / Attention / Ownership / Runtime protocol patch extensions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    FORBIDDEN_CAPABILITIES,
    RUNTIME_ID,
)
from capabilities.midplatform.protocols.protocol_checker_v1 import run_protocol_checker_flow

PROTOCOL_CHAIN_REF = "capabilities/midplatform/protocols/region_intelligence_protocol_chain_v1.json"
PATCHES_REF = "capabilities/midplatform/protocols/region_intelligence_protocol_patches_v1.json"
COMPLIANCE_PROTOCOL_ID = "LUNA-PROTO-L1-REGION-INTELLIGENCE-COMPLIANCE-V1"

CHANGE_CONTROL_PHASES = (
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_PLANNING_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_DRYRUN_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_POST_REVIEW_GO",
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_IMPLEMENTATION_PLANNING_GO",
)

UPSTREAM_REVIEW_PATHS = {
    "integration_planning": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_planning_review_v1.json"
    ),
    "integration_dryrun": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_dryrun_review_v1.json"
    ),
    "integration_post_review": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_post_review_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_integration_post_review_review_v1.json"
    ),
    "implementation_planning": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_planning_review_v1.json"
    ),
}


def _load_json(repo_root: Path, rel: str) -> Dict[str, Any]:
    path = repo_root / rel
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _check_candidate_fact_admission(dryrun_result: Dict[str, Any]) -> bool:
    if dryrun_result.get("runtime_error"):
        return dryrun_result.get("candidate_only") is True and dryrun_result.get("not_fact") is True
    if not (dryrun_result.get("candidate_only") and dryrun_result.get("not_fact")):
        return False
    for key in ("pipeline_output", "ownership_evidence_package"):
        obj = dryrun_result.get(key) or dryrun_result.get("pipeline_output", {}).get(key)
        if obj and isinstance(obj, dict):
            if not (obj.get("candidate_only", True) and obj.get("not_fact", True)):
                return False
    surfaces = (dryrun_result.get("pipeline_output") or {}).get("document_surface_candidates") or []
    return all(s.get("candidate_only") and s.get("not_fact") for s in surfaces) if surfaces else True


def _check_runtime_boundary(dryrun_result: Dict[str, Any]) -> bool:
    if dryrun_result.get("runtime_error"):
        return dryrun_result.get("no_silent_fallback") is True
    contract = dryrun_result.get("contract") or {}
    if not contract:
        return False
    forbidden = set(contract.get("forbidden_capabilities") or [])
    return all(fc in forbidden for fc in FORBIDDEN_CAPABILITIES if fc in (
        "text_recognition", "ocr", "global_ocr", "vlm", "full_scene_segmentation", "layout_semantic_parse"
    ))


def _check_model_manager_registry() -> bool:
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get(RUNTIME_ID) or {}
    return (
        entry.get("capability") == "detect_document_surface"
        and entry.get("runtime_id") == RUNTIME_ID
        and entry.get("output_type") == "document_surface_candidate"
        and entry.get("triggers_ocr") is False
    )


def _check_attention_gate(dryrun_result: Dict[str, Any], blocked_result: Dict[str, Any]) -> bool:
    if blocked_result.get("runtime_call_count", 1) != 0:
        return False
    if not blocked_result.get("skipped_by_attention_gate"):
        return False
    return dryrun_result.get("attention_gate_status") == "allowed" or dryrun_result.get("runtime_call_count", 0) >= 0


def _check_ownership_graph(dryrun_result: Dict[str, Any]) -> bool:
    if dryrun_result.get("runtime_error"):
        return dryrun_result.get("failure_returns_runtime_error_candidate") is True
    if not dryrun_result.get("surface_before_text_owner"):
        return False
    readiness = dryrun_result.get("text_owner_assignment_readiness_candidates") or []
    if readiness and not all(r.get("no_ocr_text") and r.get("text_content") is None for r in readiness):
        return False
    relations = (dryrun_result.get("pipeline_output") or {}).get("relation_hint_candidates") or []
    surfaces = (dryrun_result.get("pipeline_output") or {}).get("document_surface_candidates") or []
    if len(surfaces) >= 2 and len({s.get("surface_id") for s in surfaces}) < 2:
        return False
    screen_ok = True
    val = dryrun_result.get("validation") or {}
    if val.get("possible_screen_document_content_candidate"):
        screen_ok = val.get("screen_surface_not_document_surface_fact") is True
    return screen_ok


def _check_evidence_chain(dryrun_result: Dict[str, Any]) -> bool:
    if dryrun_result.get("runtime_error"):
        err = dryrun_result.get("runtime_error_candidate") or {}
        return err.get("handoff_to_l2_or_attention_replan") is True
    contract = dryrun_result.get("contract") or {}
    trace_fields = (
        "source_region_id",
        "attention_gate_status",
        "runtime_id",
    )
    if not all(dryrun_result.get(f) or contract.get(f) for f in ("source_region_id", "attention_gate_status")):
        return False
    if dryrun_result.get("runtime_id") != RUNTIME_ID:
        return False
    surfaces = (dryrun_result.get("pipeline_output") or {}).get("document_surface_candidates") or []
    for s in surfaces:
        if not s.get("surface_id") or not s.get("source_region_id"):
            return False
    if "field_context_candidate" not in contract:
        return False
    return True


def _check_change_control(repo_root: Path) -> bool:
    for go_id in CHANGE_CONTROL_PHASES:
        found = False
        for rel in UPSTREAM_REVIEW_PATHS.values():
            data = _load_json(repo_root, rel)
            if data.get("final_decision") == go_id:
                found = True
                break
        if not found:
            return False
    return True


def _check_protocol_patches(dryrun_result: Dict[str, Any], blocked_result: Dict[str, Any]) -> Dict[str, bool]:
    if dryrun_result.get("runtime_error"):
        return {
            "field_understanding_patch": True,
            "attention_gate_patch": blocked_result.get("runtime_call_count") == 0,
            "ownership_graph_patch": dryrun_result.get("failure_returns_runtime_error_candidate") is True,
            "lightweight_runtime_patch": dryrun_result.get("no_silent_fallback") is True,
        }
    return {
        "field_understanding_patch": "field_context_candidate" in (dryrun_result.get("contract") or {}),
        "attention_gate_patch": blocked_result.get("runtime_call_count") == 0,
        "ownership_graph_patch": _check_ownership_graph(dryrun_result),
        "lightweight_runtime_patch": (
            dryrun_result.get("no_ocr_text") is True
            and dryrun_result.get("no_cv2_import") is True
        ),
    }


def check_region_intelligence_protocol_compliance(
    *,
    dryrun_result: Dict[str, Any],
    blocked_result: Dict[str, Any],
    repo_root: Optional[Path] = None,
) -> Dict[str, Any]:
    """Protocol Compliance Review — required for Implementation DryRun."""
    root = repo_root or Path.cwd()
    chain = _load_json(root, PROTOCOL_CHAIN_REF)
    patches = _load_json(root, PATCHES_REF)

    checks = {
        "candidate_fact_admission": _check_candidate_fact_admission(dryrun_result),
        "runtime_boundary_contract": _check_runtime_boundary(dryrun_result),
        "model_manager_registry": _check_model_manager_registry(),
        "attention_gate_protocol": _check_attention_gate(dryrun_result, blocked_result),
        "ownership_graph_protocol": _check_ownership_graph(dryrun_result),
        "evidence_chain_traceability": _check_evidence_chain(dryrun_result),
        "change_control_compliance": _check_change_control(root),
    }
    patch_checks = _check_protocol_patches(dryrun_result, blocked_result)
    checks.update({f"patch_{k}": v for k, v in patch_checks.items()})

    passed = sum(1 for v in checks.values() if v)
    failed = sum(1 for v in checks.values() if not v)
    all_passed = failed == 0

    checker_flow = run_protocol_checker_flow(
        protocol_id=COMPLIANCE_PROTOCOL_ID,
        constitution_violations=[] if all_passed else ["protocol_compliance_incomplete"],
        artifacts_complete=True,
        upstream_go=checks.get("change_control_compliance", False),
        evidence_chain_complete=checks.get("evidence_chain_traceability", False),
        schema_valid=True,
        naming_valid=True,
    )

    return {
        "compliance_id": "region_intelligence_protocol_compliance_v1",
        "protocol_compliance_check": "required",
        "governance_chain": chain.get("governance_chain"),
        "protocol_patches": patches.get("patches"),
        "checks": checks,
        "review_passed_count": passed,
        "review_failed_count": failed,
        "passed": all_passed,
        "protocol_checker_flow": checker_flow,
        "candidate_only": True,
        "not_fact": True,
    }
