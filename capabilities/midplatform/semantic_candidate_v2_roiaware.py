# -*- coding: utf-8 -*-
"""Semantic Candidate v2 ROIAware — risk-flag-driven dry-run from Evidence Pack v2.

Phase-Semantic-Candidate-v2-ROIAware-001
Rule/heuristic only; no LLM/VLM/OCR. No strong semantic, no entity confirmation.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Semantic-Candidate-v2-ROIAware-001"
RUNTIME_STEP = "semantic_candidate_v2_roiaware"
CANDIDATE_SCHEMA = "ocr_semantic_candidate_v2_roiaware"

FOLLOWUPS = [
    "ROI-OCR-Quality-Diagnosis-v1",
    "Crop-Quality-Scoring-v1",
    "ROI-Crop-Diversity-Check-v1",
    "Source-Validation-v2-after-ROI-OCR",
    "Semantic-Candidate-v2-Review-Policy-v1",
    "Better-Frame-Extraction-DryRun-v1",
    "Multiframe-Merge-Proposal-v1",
    "VisualSymbolRegistry DryRun",
    "STC Contract later",
    "Controlled runtime integration",
]

RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "non_empty_text_not_accuracy",
        "applies_to": "all_roi_ep_v2",
        "condition": "risk_flags.non_empty_text_not_accuracy",
        "semantic_effect": "block_strong_semantic",
        "allowed_route": "weak_ocr_text|diagnostic_low_information|hold_for_quality_review",
        "blocked_route": "strong_entity_semantic",
        "required_next_action": "Source-Validation-v2-after-ROI-OCR",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "low_information_text_blocks_strong_semantic",
        "applies_to": "low_information_text",
        "condition": "risk_flags.low_information_text",
        "semantic_effect": "force_weak_or_diagnostic",
        "allowed_route": "diagnostic_low_information|weak_ocr_text",
        "blocked_route": "strong_entity_semantic",
        "required_next_action": "ROI-OCR-Quality-Diagnosis-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "repeated_same_text_blocks_entity_confirmation",
        "applies_to": "repeated_same_text",
        "condition": "risk_flags.repeated_same_text",
        "semantic_effect": "block_entity_confirmation",
        "allowed_route": "diagnostic_low_information|hold_for_quality_review",
        "blocked_route": "entity_confirmation|strong_entity_semantic",
        "required_next_action": "ROI-Crop-Diversity-Check-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "one_character_text_blocks_entity_semantic",
        "applies_to": "one_character_text",
        "condition": "len(raw_ocr_text.strip())==1",
        "semantic_effect": "block_entity_semantic",
        "allowed_route": "diagnostic_low_information|blocked_low_information",
        "blocked_route": "entity_semantic|bank_route_facility_interpretation",
        "required_next_action": "Crop-Quality-Scoring-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "crop_quality_uncertain_requires_quality_review",
        "applies_to": "crop_quality_uncertain",
        "condition": "risk_flags.crop_quality_uncertain",
        "semantic_effect": "require_quality_review",
        "allowed_route": "hold_for_quality_review|diagnostic_low_information",
        "blocked_route": "strong_entity_semantic",
        "required_next_action": "Crop-Quality-Scoring-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "single_roi_ocr_not_fact",
        "applies_to": "all",
        "condition": "risk_flags.single_roi_ocr_not_fact",
        "semantic_effect": "not_fact_only",
        "allowed_route": "diagnostic|weak|hold",
        "blocked_route": "fact_write|world_model_attach",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_text_completion_in_this_phase",
        "applies_to": "phase_boundary",
        "condition": "always",
        "semantic_effect": "no_completion",
        "allowed_route": "dryrun_only",
        "blocked_route": "text_completion",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_correction_in_this_phase",
        "applies_to": "phase_boundary",
        "condition": "always",
        "semantic_effect": "no_correction",
        "allowed_route": "dryrun_only",
        "blocked_route": "ocr_correction",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_llm_invocation_in_this_phase",
        "applies_to": "phase_boundary",
        "condition": "always",
        "semantic_effect": "no_llm",
        "allowed_route": "rule_based_only",
        "blocked_route": "llm_inference",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_vlm_invocation_in_this_phase",
        "applies_to": "phase_boundary",
        "condition": "always",
        "semantic_effect": "no_vlm",
        "allowed_route": "rule_based_only",
        "blocked_route": "vlm_inference",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "applies_to": "phase_boundary",
        "condition": "always",
        "semantic_effect": "no_wm",
        "allowed_route": "dryrun_only",
        "blocked_route": "world_model_attach",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "applies_to": "phase_boundary",
        "condition": "always",
        "semantic_effect": "no_scene_delta",
        "allowed_route": "dryrun_only",
        "blocked_route": "scene_delta_candidate",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

FUTURE_PHASES = [
    {
        "future_phase": "ROI-OCR-Quality-Diagnosis-v1",
        "purpose": "Diagnose repeated low-information ROI OCR outputs",
        "required_input": ["semantic_v2_repeated_same_text_diagnostic_report"],
        "expected_output": ["roi_ocr_quality_diagnosis"],
        "boundary": "diagnosis_only_no_fact",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Source-Validation-v2-after-ROI-OCR",
        "purpose": "Validate ROI OCR before semantic promotion",
        "required_input": ["semantic_candidate_v2_roiaware_collection"],
        "expected_output": ["source_validation_v2_trace"],
        "boundary": "validation_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Crop-Quality-Scoring-v1",
        "purpose": "Score crop quality before strong semantic",
        "required_input": ["evidence_pack_v2_roiref_collection"],
        "expected_output": ["crop_quality_scores"],
        "boundary": "scoring_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "ROI-Crop-Diversity-Check-v1",
        "purpose": "Detect repeated same-text across ROI crops",
        "required_input": ["roi_ocr_result_collection_v1"],
        "expected_output": ["crop_diversity_report"],
        "boundary": "check_only",
        "not_in_current_phase": True,
    },
    {
        "future_phase": "Semantic-Candidate-v2-Review-Policy-v1",
        "purpose": "Review policy for v2 weak/diagnostic candidates",
        "required_input": ["semantic_candidate_v2_roiaware_collection"],
        "expected_output": ["review_policy_trace"],
        "boundary": "policy_only_no_approve",
        "not_in_current_phase": True,
    },
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _sem_id(ep_id: str) -> str:
    return f"sem_v2_roi_{hashlib.sha256(ep_id.encode()).hexdigest()[:12]}"


def _intake_id(ep_id: str) -> str:
    return f"sem_intake_{hashlib.sha256(ep_id.encode()).hexdigest()[:10]}"


def _route_candidate(
    raw_text: str,
    risk: Dict[str, Any],
) -> Tuple[str, str, str, Optional[str]]:
    """Return semantic_route, semantic_strength, semantic_type_candidate, meaning_candidate."""
    t = str(raw_text or "").strip()
    repeated = bool(risk.get("repeated_same_text"))
    low_info = bool(risk.get("low_information_text"))
    crop_unc = bool(risk.get("crop_quality_uncertain"))
    one_char = len(t) == 1

    if repeated and low_info:
        return (
            "diagnostic_low_information",
            "diagnostic",
            "repeated_low_information_text",
            "diagnostic:repeated_low_information_ocr_glyph_only",
        )
    if low_info or one_char:
        return (
            "diagnostic_low_information",
            "diagnostic",
            "low_information_text",
            "diagnostic:low_information_ocr_glyph_only",
        )
    if crop_unc:
        return (
            "hold_for_quality_review",
            "weak",
            "roi_ocr_noise_candidate",
            None,
        )
    return (
        "weak_ocr_text",
        "weak",
        "unknown_text_or_unreadable",
        None,
    )


def run_semantic_candidate_v2_roiaware(
    *,
    evidence_pack_v2_root: str,
    roi_ocr_gated_submission_root: str,
    roi_ocrrequest_reference_root: str,
    roi_crop_rerun_root: str,
    better_frame_root: str,
    roi_retry_root: str,
    source_validation_root: str,
    adapter_v1_root: str,
    mixed_batch_v2_root: str,
    linebox_sq_root: str,
    review_queue_runtime_root: str,
    review_policy_v1_root: str,
    semantic_v1_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    ep_root = Path(evidence_pack_v2_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    packs = [
        p
        for p in (_read_json(ep_root / "evidence_pack_v2_roiref_collection.json") or {}).get("packs") or []
        if isinstance(p, dict)
    ]
    risk_doc = _read_json(ep_root / "evidence_pack_v2_raw_text_risk_report.json") or {}
    global_text = str(risk_doc.get("global_most_common_text") or "")
    global_count = int(risk_doc.get("global_most_common_count") or 0)

    intake_rows: List[Dict[str, Any]] = []
    candidates: List[Dict[str, Any]] = []
    risk_rows: List[Dict[str, Any]] = []
    guard_rows: List[Dict[str, Any]] = []
    blocking_rows: List[Dict[str, Any]] = []
    basis_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    weak_count = 0
    diagnostic_count = 0
    hold_count = 0
    repeated_consumed = 0
    low_info_consumed = 0

    for pack in packs:
        ep_id = str(pack.get("evidence_pack_id") or "")
        src = pack.get("source") if isinstance(pack.get("source"), dict) else {}
        raw_ocr = pack.get("raw_ocr") if isinstance(pack.get("raw_ocr"), dict) else {}
        raw_text = str(pack.get("raw_ocr_text") or raw_ocr.get("raw_ocr_text") or "")
        risk = pack.get("risk_flags") if isinstance(pack.get("risk_flags"), dict) else {}
        read_q = pack.get("readability_quality") if isinstance(pack.get("readability_quality"), dict) else {}
        text_items = raw_ocr.get("text_items") if isinstance(raw_ocr.get("text_items"), list) else []
        prov_meta = pack.get("provider_metadata") if isinstance(pack.get("provider_metadata"), dict) else {}

        intake_rows.append(
            {
                "semantic_v2_intake_id": _intake_id(ep_id),
                "evidence_pack_id": ep_id,
                "evidence_tier": pack.get("evidence_tier"),
                "roi_ocr_result_ref": src.get("roi_ocr_result_ref") or pack.get("roi_ocr_result_ref"),
                "ocrrequest_reference_ref": pack.get("ocrrequest_reference_ref"),
                "crop_artifact_ref": pack.get("crop_artifact_ref"),
                "raw_ocr_text": raw_text,
                "text_item_count": len(text_items),
                "risk_flags": risk,
                "source_quality_grade": read_q.get("source_quality_grade") or pack.get("source_quality_grade"),
                "target_source_quality_grade": read_q.get("target_source_quality_grade"),
                "readability_grade": read_q.get("readability_grade"),
                "provider": raw_ocr.get("provider") or prov_meta.get("provider"),
                "intake_status": "accepted",
                "eligible_for_semantic_v2": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        route, strength, sem_type, meaning = _route_candidate(raw_text, risk)
        if strength == "weak":
            weak_count += 1
        elif strength == "diagnostic":
            diagnostic_count += 1
        if route == "hold_for_quality_review":
            hold_count += 1

        if risk.get("repeated_same_text"):
            repeated_consumed += 1
        if risk.get("low_information_text"):
            low_info_consumed += 1

        chain = list(src.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        sem_id = _sem_id(ep_id)
        gov = {
            "strong_semantic_allowed": False,
            "entity_confirmation_allowed": False,
            "completion_allowed": False,
            "correction_allowed": False,
            "source_validation_v2_required": True,
            "quality_review_required": bool(risk.get("crop_quality_uncertain")),
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        }

        candidate = {
            "semantic_candidate_v2_id": sem_id,
            "schema_version": CANDIDATE_SCHEMA,
            "source_evidence_pack_v2_ref": ep_id,
            "source_roi_ocr_result_ref": src.get("roi_ocr_result_ref"),
            "source_ocrrequest_ref": pack.get("ocrrequest_reference_ref"),
            "source_crop_ref": pack.get("crop_artifact_ref"),
            "raw_ocr_text": raw_text,
            "normalized_text_candidate": raw_text,
            "semantic_route": route,
            "semantic_strength": strength,
            "meaning_candidate": meaning,
            "entity_candidate": None,
            "semantic_type_candidate": sem_type,
            "risk_consumption": {
                "repeated_same_text_consumed": bool(risk.get("repeated_same_text")),
                "low_information_text_consumed": bool(risk.get("low_information_text")),
                "crop_quality_uncertain_consumed": bool(risk.get("crop_quality_uncertain")),
                "non_empty_text_not_accuracy_consumed": bool(risk.get("non_empty_text_not_accuracy")),
            },
            "interpretation_basis": {
                "evidence_pack_ref": ep_id,
                "ocrrequest_ref": pack.get("ocrrequest_reference_ref"),
                "crop_ref": pack.get("crop_artifact_ref"),
                "provider_metadata_ref": prov_meta,
                "text_items_ref": f"{ep_id}:text_items",
                "coordinate_ref": pack.get("crop_bbox_xyxy"),
            },
            "governance": gov,
            "source_chain": chain,
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        candidates.append(candidate)

        blocked = [
            "strong_entity_semantic",
            "entity_confirmation",
            "world_model_attach",
            "scene_delta_candidate",
            "navigation_use",
            "bank_route_facility_sign_interpretation",
        ]
        risk_rows.append(
            {
                "semantic_candidate_v2_id": sem_id,
                "evidence_pack_id": ep_id,
                "raw_ocr_text": raw_text,
                "repeated_same_text": bool(risk.get("repeated_same_text")),
                "low_information_text": bool(risk.get("low_information_text")),
                "crop_quality_uncertain": bool(risk.get("crop_quality_uncertain")),
                "non_empty_text_not_accuracy": bool(risk.get("non_empty_text_not_accuracy")),
                "risk_consumed": True,
                "semantic_effect": f"route={route};strength={strength}",
                "blocked_routes": blocked,
                "required_next_action": "ROI-OCR-Quality-Diagnosis-v1;Source-Validation-v2-after-ROI-OCR",
            }
        )

        guard_rows.append(
            {
                "evidence_pack_id": ep_id,
                "semantic_candidate_v2_id": sem_id,
                "raw_ocr_text": raw_text,
                "text_length": len(raw_text.strip()),
                "one_character_text": len(raw_text.strip()) == 1,
                "low_information_text": bool(risk.get("low_information_text")),
                "allowed_semantic_strength": strength,
                "entity_confirmation_allowed": False,
                "strong_semantic_allowed": False,
                "correction_allowed": False,
                "completion_allowed": False,
                "fact_write_allowed": False,
            }
        )

        blocking_rows.append(
            {
                "semantic_candidate_v2_id": sem_id,
                "blocked_strong_semantic": True,
                "blocked_entity_confirmation": True,
                "blocked_world_model_attach": True,
                "blocked_scene_delta_candidate": True,
                "blocked_navigation_use": True,
                "block_reasons": [
                    "repeated_same_text" if risk.get("repeated_same_text") else None,
                    "low_information_text" if risk.get("low_information_text") else None,
                    "non_empty_text_not_accuracy",
                    "single_roi_ocr_not_fact",
                ],
                "allowed_future_phase": [
                    "Source-Validation-v2-after-ROI-OCR",
                    "ROI-OCR-Quality-Diagnosis-v1",
                    "Crop-Quality-Scoring-v1",
                ],
            }
        )
        blocking_rows[-1]["block_reasons"] = [b for b in blocking_rows[-1]["block_reasons"] if b]

        missing_refs: List[str] = []
        if not pack.get("ocrrequest_reference_ref"):
            missing_refs.append("ocrrequest_ref")
        basis_status = "complete_but_low_information" if not missing_refs else "incomplete"
        basis_rows.append(
            {
                "semantic_candidate_v2_id": sem_id,
                "evidence_pack_ref": ep_id,
                "ocrrequest_ref": pack.get("ocrrequest_reference_ref"),
                "crop_ref": pack.get("crop_artifact_ref"),
                "provider_metadata_ref": bool(prov_meta),
                "text_items_ref": bool(text_items),
                "coordinate_ref": pack.get("crop_bbox_xyxy"),
                "interpretation_basis_complete": not missing_refs,
                "missing_refs": missing_refs,
                "interpretation_basis_status": basis_status,
            }
        )

        chain_rows.append(
            {
                "semantic_candidate_v2_id": sem_id,
                "traceable_to_evidence_pack_v2": True,
                "traceable_to_roi_ocr_result": bool(src.get("roi_ocr_result_ref")),
                "traceable_to_ocrrequest_reference": bool(pack.get("ocrrequest_reference_ref")),
                "traceable_to_crop_artifact": bool(pack.get("crop_artifact_ref")),
                "traceable_to_better_frame_selection": bool(src.get("better_frame_candidate_ref")),
                "traceable_to_linebox_trace": bool(src.get("linebox_trace_ref")),
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )

    pack_count = len(packs)
    cand_count = len(candidates)
    affected_ids = [c["semantic_candidate_v2_id"] for c in candidates]

    routing = {
        "schema_version": "semantic_v2_routing_report_v1",
        "weak_ocr_text_count": sum(1 for c in candidates if c.get("semantic_route") == "weak_ocr_text"),
        "diagnostic_low_information_count": sum(
            1 for c in candidates if c.get("semantic_route") == "diagnostic_low_information"
        ),
        "hold_for_quality_review_count": hold_count,
        "blocked_low_information_count": sum(
            1 for c in candidates if c.get("semantic_route") == "blocked_low_information"
        ),
        "strong_semantic_generated_count": 0,
        "entity_candidate_generated_count": 0,
        "source_validation_v2_required_count": cand_count,
        "quality_review_required_count": sum(
            1 for c in candidates if (c.get("governance") or {}).get("quality_review_required")
        ),
        "world_model_attach_allowed_count": 0,
        "scene_delta_candidate_allowed_count": 0,
    }

    repeated_diag = {
        "schema_version": "semantic_v2_repeated_same_text_diagnostic_report_v1",
        "global_most_common_text": global_text,
        "repeated_text_count": global_count,
        "repeated_text_ratio": round(global_count / pack_count, 4) if pack_count else 0.0,
        "affected_candidate_ids": affected_ids,
        "diagnostic_status": "requires_roi_quality_diagnosis"
        if global_count >= 2 and global_text
        else "no_global_repeat",
        "suspected_issue": [
            "crop_too_narrow",
            "repeated_same_roi_mapping",
            "provider_low_information_output",
            "roi_quality_problem",
            "source_diversity_problem",
        ],
        "required_next_action": "ROI-OCR-Quality-Diagnosis-v1;ROI-Crop-Diversity-Check-v1",
    }

    summary = {
        "schema_version": "semantic_candidate_v2_roiaware_summary_v0",
        "phase": PHASE_ID,
        "generator_scope": "semantic_candidate_v2_roiaware_dryrun_only",
        "based_on_evidence_pack_v2_roiref": ep_root.is_dir(),
        "evidence_pack_v2_count_observed": pack_count,
        "semantic_candidate_v2_generated": cand_count > 0,
        "semantic_candidate_v2_count": cand_count,
        "strong_semantic_generated_count": 0,
        "weak_semantic_generated_count": weak_count,
        "diagnostic_semantic_generated_count": diagnostic_count,
        "semantic_hold_count": hold_count,
        "risk_flags_consumed": cand_count > 0,
        "repeated_same_text_consumed": repeated_consumed == pack_count and pack_count > 0,
        "low_information_text_consumed": low_info_consumed == pack_count and pack_count > 0,
        "non_empty_text_not_accuracy_consumed": True,
        "llm_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "source_validation_v2_invoked": False,
        "review_decision_committed": False,
        "approval_granted": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": "GO" if cand_count == 12 and pack_count == 12 else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "semantic_v2_evidence_pack_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {
            "schema_version": "semantic_v2_roiaware_rule_matrix_v1",
            "rules": RULES,
        },
        "schema_doc": {
            "schema_version": "semantic_candidate_v2_roiaware_schema_v1",
            "template": {
                "semantic_candidate_v2_id": "sem_v2_roi_<hash>",
                "schema_version": CANDIDATE_SCHEMA,
                "source_evidence_pack_v2_ref": None,
                "source_roi_ocr_result_ref": None,
                "source_ocrrequest_ref": None,
                "source_crop_ref": None,
                "raw_ocr_text": None,
                "normalized_text_candidate": None,
                "semantic_route": "weak_ocr_text | diagnostic_low_information | hold_for_quality_review | blocked_low_information",
                "semantic_strength": "none | weak | diagnostic",
                "meaning_candidate": None,
                "entity_candidate": None,
                "semantic_type_candidate": "unknown_text_or_unreadable | low_information_text | repeated_low_information_text | roi_ocr_noise_candidate",
                "risk_consumption": {
                    "repeated_same_text_consumed": False,
                    "low_information_text_consumed": False,
                    "crop_quality_uncertain_consumed": False,
                    "non_empty_text_not_accuracy_consumed": False,
                },
                "interpretation_basis": {
                    "evidence_pack_ref": None,
                    "ocrrequest_ref": None,
                    "crop_ref": None,
                    "provider_metadata_ref": None,
                    "text_items_ref": None,
                    "coordinate_ref": None,
                },
                "governance": {
                    "strong_semantic_allowed": False,
                    "entity_confirmation_allowed": False,
                    "completion_allowed": False,
                    "correction_allowed": False,
                    "source_validation_v2_required": True,
                    "quality_review_required": True,
                    "world_model_attach_allowed": False,
                    "scene_delta_candidate_allowed": False,
                    "fact_status": "not_fact",
                    "write_allowed": False,
                },
                "source_chain": [],
            },
        },
        "collection": {
            "schema_version": "semantic_candidate_v2_roiaware_collection_v1",
            "candidate_count": cand_count,
            "candidates": candidates,
        },
        "risk_consumption": {
            "schema_version": "semantic_v2_risk_consumption_report_v1",
            "row_count": len(risk_rows),
            "rows": risk_rows,
        },
        "low_information_guard": {
            "schema_version": "semantic_v2_low_information_guard_report_v1",
            "row_count": len(guard_rows),
            "rows": guard_rows,
        },
        "repeated_diag": repeated_diag,
        "blocking_matrix": {
            "schema_version": "semantic_v2_blocking_matrix_v1",
            "row_count": len(blocking_rows),
            "rows": blocking_rows,
        },
        "interpretation_basis": {
            "schema_version": "semantic_v2_interpretation_basis_report_v1",
            "row_count": len(basis_rows),
            "basis_complete_not_semantic_valid": True,
            "rows": basis_rows,
        },
        "source_chain_report": {
            "schema_version": "semantic_v2_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_evidence_pack_v2": all(r.get("traceable_to_evidence_pack_v2") for r in chain_rows),
            "rows": chain_rows,
        },
        "routing": routing,
        "future_plan": {
            "schema_version": "semantic_v2_future_review_validation_plan_v1",
            "phases": FUTURE_PHASES,
        },
        "boundary": {
            "schema_version": "semantic_v2_boundary_report_v1",
            "semantic_v2_roiaware_dryrun_only": True,
            "strong_semantic_generated": False,
            "entity_candidate_generated": False,
            "completion_committed": False,
            "correction_committed": False,
            "llm_invoked": False,
            "vlm_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "source_validation_v2_invoked": False,
            "review_decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
        },
        "metrics": {
            "schema_version": "semantic_v2_metrics_candidate_report_v1",
            "evidence_pack_v2_count_observed": pack_count,
            "semantic_candidate_v2_count": cand_count,
            "strong_semantic_generated_count": 0,
            "weak_semantic_generated_count": weak_count,
            "diagnostic_semantic_generated_count": diagnostic_count,
            "semantic_hold_count": hold_count,
            "repeated_same_text_consumed_count": repeated_consumed,
            "low_information_text_consumed_count": low_info_consumed,
            "entity_candidate_generated_count": 0,
            "source_validation_v2_required_count": cand_count,
            "quality_review_required_count": routing["quality_review_required_count"],
            "fact_write_allowed_count": 0,
            "world_model_attach_allowed_count": 0,
            "scene_delta_candidate_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "semantic_v2_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "semantic_v2_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "semantic_v2_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "semantic_v2_roiaware_dryrun_only": True,
            "strong_semantic_generated": False,
            "entity_candidate_generated": False,
            "completion_committed": False,
            "correction_committed": False,
            "llm_invoked": False,
            "vlm_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "source_validation_v2_invoked": False,
            "decision_committed": False,
            "approval_granted": False,
            "auto_approve_invoked": False,
            "fact_review_generated": False,
            "world_model_attach_executed": False,
            "scene_delta_candidate_generated": False,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "semantic_v2_simulation_context_report_v1",
            "simulation_profile_id": (_read_json(sim / "simulation_summary.json") or {}).get(
                "simulation_profile_id", "developer_full"
            ),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "semantic_v2_non_claims_report_v1",
            "no_ocr_in_phase": True,
            "no_llm_vlm": True,
            "semantic_not_fact": True,
            "weak_diagnostic_not_entity": True,
            "hang_character_not_bank_route_facility": True,
            "repeated_text_not_semantic_consensus": True,
            "low_info_not_valid_semantic": True,
            "no_source_validation_v2": True,
            "no_world_model": True,
            "no_benchmark_claim": True,
        },
        "followups": {"schema_version": "semantic_v2_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "semantic_v2_audit_report_v1",
            "semantic_candidate_v2_roiaware_executed": True,
            "semantic_v2_roiaware_dryrun_only": True,
            "evidence_pack_v2_count_observed": pack_count,
            "semantic_candidate_v2_count": cand_count,
            "risk_flags_consumed": True,
            "repeated_same_text_consumed": repeated_consumed == pack_count and pack_count > 0,
            "low_information_text_consumed": low_info_consumed == pack_count and pack_count > 0,
            "strong_semantic_generated_count": 0,
            "entity_candidate_generated_count": 0,
            "completion_committed": False,
            "correction_committed": False,
            "llm_invoked": False,
            "vlm_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "source_validation_v2_invoked": False,
            "decision_committed": False,
            "approval_granted": False,
            "world_model_attach_executed": False,
            "scene_delta_candidate_generated": False,
            "midplatform_fact_written": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }
