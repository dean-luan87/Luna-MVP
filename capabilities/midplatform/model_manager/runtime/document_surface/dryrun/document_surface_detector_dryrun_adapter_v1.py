# -*- coding: utf-8 -*-
"""Document Surface Detector — dryrun adapter v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    RUNTIME_ID,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_detector_fixture_runtime_v1 import (
    run_document_surface_fixture_runtime,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_evidence_package_builder_v1 import (
    build_document_surface_evidence_package,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_runtime_binding_v1 import (
    bind_document_surface_runtime,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_text_owner_assignment_adapter_v1 import (
    build_text_owner_assignment_candidates,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_to_ownership_adapter_v1 import (
    adapt_surfaces_to_ownership_entities,
)
from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_validation_adapter_v1 import (
    resolve_validation_status,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_DRYRUN_BLOCKED"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_document_surface_detector_dryrun(
    *,
    fixture_ref: str = "stacked_papers",
    source_region_id: str = "region_001",
    attention_gate_status: str = "allowed",
    runtime_unavailable: bool = False,
) -> Dict[str, Any]:
    """
    DryRun governance loop:
    Attention-Gated Region → Runtime Binding → Fixture Runtime → Evidence → Validation
    """
    if runtime_unavailable:
        return {
            "dryrun_only": True,
            "fixture_ref": fixture_ref,
            "document_surface_dryrun_result": {
                "source_region_id": source_region_id,
                "attention_gate_status": attention_gate_status,
                "runtime_id": RUNTIME_ID,
                "document_surface_runtime_error_candidate": {
                    "error_id": _uid("dsre"),
                    "error_type": "document_surface_runtime_unavailable",
                    "handoff_to_l2_or_attention_replan": True,
                    "candidate_only": True,
                },
                "candidate_only": True,
                "not_fact": True,
            },
            "no_silent_fallback_to_ocr": True,
            "no_silent_fallback_to_vlm": True,
            "no_full_scene_segmentation_fallback": True,
            "failure_returns_runtime_error_candidate": True,
            "governance_loop_complete": True,
            "candidate_only": True,
            "not_fact": True,
        }

    binding = bind_document_surface_runtime(
        attention_gate_status=attention_gate_status,
        source_region_id=source_region_id,
    )

    if binding.get("runtime_binding_status_candidate") == "skipped_by_attention_gate":
        return {
            "dryrun_only": True,
            "fixture_ref": fixture_ref,
            "document_surface_dryrun_result": {
                "source_region_id": source_region_id,
                "attention_gate_status": attention_gate_status,
                "runtime_id": RUNTIME_ID,
                "runtime_binding_status_candidate": "skipped_by_attention_gate",
                "runtime_call_count": 0,
                "runtime_status_candidate": "skipped_by_attention_gate",
                "document_surface_candidates": [],
                "relation_hint_candidates": [],
                "ownership_evidence_package": None,
                "text_owner_assignment_candidates": [],
                "validation_status_candidate": "skipped_by_attention_gate",
                "candidate_only": True,
                "not_fact": True,
            },
            "attention_blocked_zero_runtime_call": True,
            "governance_loop_complete": True,
            "candidate_only": True,
            "not_fact": True,
        }

    runtime_out = run_document_surface_fixture_runtime(
        fixture_ref=fixture_ref,
        source_region_id=source_region_id,
    )
    ownership = adapt_surfaces_to_ownership_entities(
        document_surface_candidates=runtime_out.get("document_surface_candidates") or [],
        relation_hint_candidates=runtime_out.get("relation_hint_candidates") or [],
        source_region_id=source_region_id,
    )
    text_assignments = build_text_owner_assignment_candidates(
        document_surface_candidates=runtime_out.get("document_surface_candidates") or [],
        relation_hint_candidates=runtime_out.get("relation_hint_candidates") or [],
    )
    validation = resolve_validation_status(
        runtime_status=runtime_out.get("runtime_status_candidate", "ok"),
        layout_conflict=runtime_out.get("layout_conflict_detected", False),
        possible_screen_document=runtime_out.get("possible_screen_document_content", False),
        request_more_evidence=runtime_out.get("request_more_evidence_candidate", False),
    )

    evidence_pkg = build_document_surface_evidence_package(
        source_region_id=source_region_id,
        attention_gate_status=attention_gate_status,
        document_surface_candidates=runtime_out.get("document_surface_candidates") or [],
        relation_hint_candidates=runtime_out.get("relation_hint_candidates") or [],
        entity_candidates=ownership.get("entity_candidates") or [],
        text_owner_assignment_candidates=text_assignments,
        validation_status_candidate=validation.get("validation_status_candidate", "pending_validation"),
        next_slot_candidate=runtime_out.get("next_slot_candidate"),
    )

    dryrun_result = {
        "dryrun_id": _uid("dsdr"),
        "source_region_id": source_region_id,
        "attention_gate_status": attention_gate_status,
        "runtime_id": RUNTIME_ID,
        "runtime_binding_status_candidate": binding.get("runtime_binding_status_candidate"),
        "runtime_call_count": binding.get("runtime_call_count", 1),
        "runtime_status_candidate": runtime_out.get("runtime_status_candidate"),
        "document_surface_candidates": runtime_out.get("document_surface_candidates") or [],
        "relation_hint_candidates": runtime_out.get("relation_hint_candidates") or [],
        "ownership_evidence_package": evidence_pkg,
        "text_owner_assignment_candidates": text_assignments,
        "validation_status_candidate": validation.get("validation_status_candidate"),
        "next_slot_candidate": runtime_out.get("next_slot_candidate"),
        "layout_conflict_detected": runtime_out.get("layout_conflict_detected", False),
        "possible_screen_document_content": runtime_out.get("possible_screen_document_content", False),
        "request_more_evidence_candidate": validation.get("request_more_evidence_candidate", False),
        "candidate_only": True,
        "not_fact": True,
    }

    return {
        "dryrun_only": True,
        "fixture_ref": fixture_ref,
        "runtime_binding": binding,
        "runtime_output": runtime_out,
        "ownership_adaptation": ownership,
        "validation": validation,
        "document_surface_dryrun_result": dryrun_result,
        "no_ocr_text_output": True,
        "surface_before_text_owner": True,
        "owner_required_for_text_assignment": all(
            a.get("owner_required_for_assignment") for a in text_assignments
        ) if text_assignments else True,
        "attention_gate_required": True,
        "no_global_ocr": True,
        "governance_loop_complete": True,
        "candidate_only": True,
        "not_fact": True,
    }
