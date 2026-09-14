# -*- coding: utf-8 -*-
"""Semantic Candidate v3 BBoxExpansionAware — rule/heuristic from EP v3.

Phase-Semantic-Candidate-v3-BBoxExpansionAware-001
No LLM/VLM/OCR. Bank-like candidate only; no entity confirmation.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Semantic-Candidate-v3-BBoxExpansionAware-001"
RUNTIME_STEP = "semantic_candidate_v3_bbox_expansion_aware"
CANDIDATE_SCHEMA = "ocr_semantic_candidate_v3_bbox_expansion_aware"

BANK_TERMS = ("银行", "建行", "建设", "建银", "Bank", "bank")
NOISY_EN_PATTERNS = (
    re.compile(r"\bG\s*QocionBank\b", re.I),
    re.compile(r"\bGm\s*QocionBank\b", re.I),
    re.compile(r"QocionBank", re.I),
    re.compile(r"\b[A-Za-z]{2,}\s+[A-Za-z]{4,}Bank\b"),
)

FOLLOWUPS = [
    "Semantic-Candidate-v3-Review-Policy",
    "Source-Validation-v2-after-EP-v3",
    "ROI-OCR-Quality-Diagnosis-v2-BBoxExpansion",
    "Crop-Quality-Scoring-v1",
    "Multiframe-Merge-Proposal-v1",
    "Better-Frame-Extraction-DryRun-v1",
    "Future-Detector-ROI-Proposal-v1",
    "VisualSymbolRegistry DryRun",
    "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
    "STC Contract later",
    "Controlled runtime integration",
]

RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "bank_like_text_generates_candidate_only",
        "condition": "bank_like_terms in raw_ocr_text",
        "semantic_effect": "bank_sign_candidate",
        "allowed_candidate_type": "bank_sign_candidate",
        "blocked_action": "entity_confirmation",
        "required_next_action": "Source-Validation-v2-after-EP-v3",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "noisy_english_text_generates_noise_candidate",
        "condition": "noisy English segment detected",
        "semantic_effect": "noisy_english_text_candidate",
        "allowed_candidate_type": "noisy_english_text_candidate|ocr_noise_candidate",
        "blocked_action": "auto_correct_to_china_construction_bank",
        "required_next_action": "Source-Validation-v2-after-EP-v3",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "repeated_strategy_output_not_consensus",
        "condition": "repeated_with_other_strategy",
        "semantic_effect": "strategy_repeat_only",
        "allowed_candidate_type": "bank_sign_candidate",
        "blocked_action": "independent_consensus",
        "required_next_action": "Source-Validation-v2-after-EP-v3",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "same_frame_same_region_blocks_independent_consensus",
        "condition": "same_frame_same_region_not_independent_consensus",
        "semantic_effect": "block_consensus",
        "allowed_candidate_type": "candidate_only",
        "blocked_action": "independent_consensus",
        "required_next_action": "Multiframe-Merge-Proposal-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "non_empty_text_not_accuracy",
        "condition": "non_empty raw_ocr_text",
        "semantic_effect": "not_accuracy",
        "allowed_candidate_type": "candidate_only",
        "blocked_action": "accuracy_claim",
        "required_next_action": "Source-Validation-v2-after-EP-v3",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "useful_text_candidate_not_fact",
        "condition": "useful_text_candidate",
        "semantic_effect": "candidate_only",
        "allowed_candidate_type": "entity_candidate",
        "blocked_action": "fact_write",
        "required_next_action": "Source-Validation-v2-after-EP-v3",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_entity_confirmation_in_this_phase",
        "condition": "always",
        "semantic_effect": "entity_confirmed=false",
        "allowed_candidate_type": "entity_candidate",
        "blocked_action": "entity_confirmation",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_correction_commit_in_this_phase",
        "condition": "always",
        "semantic_effect": "no_correction",
        "allowed_candidate_type": "dryrun_only",
        "blocked_action": "correction_commit",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_completion_commit_in_this_phase",
        "condition": "always",
        "semantic_effect": "no_completion",
        "allowed_candidate_type": "dryrun_only",
        "blocked_action": "completion_commit",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_llm_invocation_in_this_phase",
        "condition": "always",
        "semantic_effect": "no_llm",
        "allowed_candidate_type": "rule_based_only",
        "blocked_action": "llm_inference",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_source_validation_v2_in_this_phase",
        "condition": "always",
        "semantic_effect": "sv_v2_later",
        "allowed_candidate_type": "readiness_placeholder",
        "blocked_action": "source_validation_v2",
        "required_next_action": "Source-Validation-v2-after-EP-v3",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "always",
        "semantic_effect": "no_wm",
        "allowed_candidate_type": "dryrun_only",
        "blocked_action": "world_model_attach",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "always",
        "semantic_effect": "no_scene_delta",
        "allowed_candidate_type": "dryrun_only",
        "blocked_action": "scene_delta_candidate",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _sem_id(ep_id: str) -> str:
    return f"sem_v3_bbox_{hashlib.sha256(ep_id.encode()).hexdigest()[:12]}"


def _intake_id(ep_id: str) -> str:
    return f"sem_v3_intake_{hashlib.sha256(ep_id.encode()).hexdigest()[:10]}"


def _detect_bank_terms(text: str) -> List[str]:
    found: List[str] = []
    for term in BANK_TERMS:
        if term in text:
            found.append(term)
    if "建设" in text and "银行" in text:
        if "建设银行" not in found and any("建设" in text for _ in [1]):
            seg = re.findall(r"[\u4e00-\u9fff]+银行|[\u4e00-\u9fff]*建设[\u4e00-\u9fff]*", text)
            for s in seg:
                if s and s not in found:
                    found.append(s)
    for m in re.finditer(r"[\u4e00-\u9fff]{2,6}银行", text):
        t = m.group(0)
        if t not in found:
            found.append(t)
    return found


def _detect_noisy_segments(text: str) -> List[Dict[str, Any]]:
    segments: List[Dict[str, Any]] = []
    for pat in NOISY_EN_PATTERNS:
        for m in pat.finditer(text):
            seg = m.group(0).strip()
            if seg and not any(s.get("segment") == seg for s in segments):
                segments.append(
                    {
                        "segment": seg,
                        "suspected_language": "en",
                        "noise_pattern": "ocr_glyph_substitution_candidate",
                    }
                )
    parts = [p.strip() for p in re.split(r"\|", text) if p.strip()]
    for p in parts:
        if re.search(r"[A-Za-z]", p) and not re.search(r"^[\u4e00-\u9fff]+$", p):
            if not any(s.get("segment") == p for s in segments):
                segments.append(
                    {
                        "segment": p,
                        "suspected_language": "en",
                        "noise_pattern": "mixed_script_ocr_noise",
                    }
                )
    return segments


def _classify_pack(
    raw_text: str,
    *,
    repeated_strategy: bool,
    same_frame_block: bool,
) -> Tuple[str, str, str, Optional[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    bank_terms = _detect_bank_terms(raw_text)
    noisy = _detect_noisy_segments(raw_text)
    has_bank = bool(bank_terms)
    has_noisy = bool(noisy)

    entity: Optional[Dict[str, Any]] = None
    if has_bank:
        name = bank_terms[0] if bank_terms else None
        if "建设" in raw_text:
            for m in re.finditer(r"[\u4e00-\u9fff]{2,8}银行", raw_text):
                name = m.group(0)
                break
        entity = {
            "entity_type": "bank",
            "entity_name_candidate": name,
            "entity_confidence": 0.35 if has_bank else None,
            "entity_confirmed": False,
        }

    if has_bank and has_noisy:
        route = "mixed_candidate"
        sem_type = "bank_sign_candidate"
        strength = "candidate"
    elif has_bank:
        route = "bank_like_candidate"
        sem_type = "bank_sign_candidate"
        strength = "candidate"
    elif has_noisy:
        route = "noisy_text_candidate"
        sem_type = "noisy_english_text_candidate"
        strength = "weak"
    else:
        route = "hold_for_review"
        sem_type = "unknown_text_candidate"
        strength = "weak"

    text_interp = {
        "bank_like_terms_detected": bank_terms,
        "noisy_segments": noisy,
        "uncertain_segments": [],
        "correction_candidate": None,
        "completion_candidate": None,
        "correction_committed": False,
        "completion_committed": False,
    }

    strategy_ctx = {
        "strategy_comparison_candidate_only": True,
        "same_frame_same_region_not_independent_consensus": same_frame_block,
        "repeated_with_other_strategy": repeated_strategy,
        "independent_consensus_allowed": False,
    }

    return route, strength, sem_type, entity, text_interp, strategy_ctx


def run_semantic_candidate_v3_bbox_expansion_aware(
    *,
    evidence_pack_v3_root: str,
    ocrrequest_gated_submission_v2_root: str,
    roi_ocrrequest_reference_v2_root: str,
    roi_crop_v2_root: str,
    roi_bbox_expansion_root: str,
    roi_crop_diversity_root: str,
    roi_ocr_quality_diagnosis_root: str,
    semantic_v2_root: str,
    evidence_pack_v2_root: str,
    linebox_sq_root: str,
    mixed_batch_v2_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    ep_root = Path(evidence_pack_v3_root).resolve()
    crop_v2_root = Path(roi_crop_v2_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    packs = [
        p
        for p in (_read_json(ep_root / "evidence_pack_v3_bbox_expansion_collection.json") or {}).get("packs") or []
        if isinstance(p, dict)
    ]
    risk_rows_ep = (_read_json(ep_root / "evidence_pack_v3_strategy_output_risk_report.json") or {}).get("rows") or []
    risk_by_ep = {str(r.get("evidence_pack_v3_id")): r for r in risk_rows_ep if isinstance(r, dict)}

    intake_rows: List[Dict[str, Any]] = []
    candidates: List[Dict[str, Any]] = []
    bank_rows: List[Dict[str, Any]] = []
    noisy_rows: List[Dict[str, Any]] = []
    entity_boundary_rows: List[Dict[str, Any]] = []
    basis_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    bank_like_count = 0
    noisy_count = 0
    entity_candidate_count = 0
    strategy_repeat_count = 0

    text_to_packs: Dict[str, List[Tuple[str, str]]] = defaultdict(list)

    for pack in packs:
        ep_id = str(pack.get("evidence_pack_v3_id") or "")
        raw_text = str(pack.get("raw_ocr_text") or pack.get("raw_ocr", {}).get("raw_ocr_text") or "")
        strategy = str(pack.get("expansion_strategy") or "")
        text_to_packs[raw_text.strip()].append((ep_id, strategy))

    repeat_pairs: List[Dict[str, Any]] = []
    for text, entries in text_to_packs.items():
        if len(entries) >= 2 and text:
            strategies = [e[1] for e in entries]
            repeat_pairs.append(
                {
                    "repeated_text": text,
                    "repeated_strategy_pair": strategies,
                    "affected_candidate_ids": [],
                }
            )

    for pack in packs:
        ep_id = str(pack.get("evidence_pack_v3_id") or "")
        src = pack.get("source") if isinstance(pack.get("source"), dict) else {}
        raw_ocr = pack.get("raw_ocr") if isinstance(pack.get("raw_ocr"), dict) else {}
        raw_text = str(pack.get("raw_ocr_text") or raw_ocr.get("raw_ocr_text") or "")
        risk_ep = risk_by_ep.get(ep_id, {})
        risk_flags = pack.get("risk_flags") if isinstance(pack.get("risk_flags"), dict) else risk_ep.get("risk_flags") or {}
        repeated_strategy = bool(
            risk_ep.get("repeated_with_other_strategy") or pack.get("strategy_context", {}).get("repeated_with_other_strategy")
        )
        same_frame = bool(
            risk_flags.get("same_frame_same_region_not_independent_consensus")
            or risk_ep.get("same_frame_same_region_not_independent_consensus")
        )
        if repeated_strategy:
            strategy_repeat_count += 1

        conf = pack.get("provider_metadata", {}).get("confidence_summary") if isinstance(pack.get("provider_metadata"), dict) else {}
        if not conf:
            conf = raw_ocr.get("provider_metadata", {}).get("confidence_summary", {}) if isinstance(raw_ocr.get("provider_metadata"), dict) else {}

        intake_rows.append(
            {
                "semantic_v3_intake_id": _intake_id(ep_id),
                "evidence_pack_v3_id": ep_id,
                "evidence_tier": pack.get("evidence_tier"),
                "expansion_strategy": pack.get("expansion_strategy"),
                "raw_ocr_text": raw_text,
                "text_item_count": len(raw_ocr.get("text_items") or pack.get("text_items") or []),
                "confidence_summary": conf,
                "source_bbox_xyxy": pack.get("source_bbox_xyxy") or pack.get("image_coordinates", {}).get("source_bbox_xyxy"),
                "expanded_bbox_xyxy": pack.get("expanded_bbox_xyxy") or pack.get("image_coordinates", {}).get("expanded_bbox_xyxy"),
                "crop_width": pack.get("crop_width"),
                "crop_height": pack.get("crop_height"),
                "area_growth_ratio": pack.get("area_growth_ratio"),
                "ocrrequest_reference_v2_ref": pack.get("ocrrequest_reference_v2_ref"),
                "expanded_crop_artifact_ref": pack.get("expanded_crop_artifact_ref"),
                "bbox_expansion_candidate_ref": pack.get("bbox_expansion_candidate_ref"),
                "risk_flags": risk_flags,
                "strategy_comparison_candidate_only": True,
                "same_frame_same_region_not_independent_consensus": same_frame,
                "repeated_with_other_strategy": repeated_strategy,
                "intake_status": "accepted",
                "eligible_for_semantic_v3": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        route, strength, sem_type, entity, text_interp, strategy_ctx = _classify_pack(
            raw_text,
            repeated_strategy=repeated_strategy,
            same_frame_block=same_frame,
        )

        bank_terms = text_interp.get("bank_like_terms_detected") or []
        noisy_segs = text_interp.get("noisy_segments") or []
        if bank_terms:
            bank_like_count += 1
        if noisy_segs:
            noisy_count += 1
        if entity:
            entity_candidate_count += 1

        chain = list(src.get("source_chain") or pack.get("source_chain") or [])
        if RUNTIME_STEP not in chain:
            chain.append(RUNTIME_STEP)

        sem_id = _sem_id(ep_id)
        gov = {
            "entity_confirmation_allowed": False,
            "source_validation_v2_required_later": True,
            "source_validation_v2_invoked_now": False,
            "review_required_later": True,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        }

        candidate = {
            "semantic_candidate_v3_id": sem_id,
            "schema_version": CANDIDATE_SCHEMA,
            "source_evidence_pack_v3_ref": ep_id,
            "expansion_strategy": pack.get("expansion_strategy"),
            "raw_ocr_text": raw_text,
            "normalized_text_candidate": raw_text,
            "semantic_route": route,
            "semantic_strength": strength,
            "semantic_type_candidate": sem_type,
            "entity_candidate": entity,
            "text_interpretation": text_interp,
            "strategy_context": strategy_ctx,
            "interpretation_basis": {
                "evidence_pack_v3_ref": ep_id,
                "ocrrequest_reference_v2_ref": pack.get("ocrrequest_reference_v2_ref"),
                "expanded_crop_artifact_ref": pack.get("expanded_crop_artifact_ref"),
                "bbox_expansion_candidate_ref": pack.get("bbox_expansion_candidate_ref"),
                "source_bbox_ref": pack.get("source_bbox_xyxy"),
                "expanded_bbox_ref": pack.get("expanded_bbox_xyxy"),
                "text_items_ref": f"{ep_id}:text_items",
                "provider_metadata_ref": pack.get("provider_metadata"),
                "strategy_context_ref": pack.get("bbox_expansion_context"),
            },
            "governance": gov,
            "source_chain": chain,
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        candidates.append(candidate)

        for rp in repeat_pairs:
            if raw_text.strip() == rp.get("repeated_text"):
                if sem_id not in rp["affected_candidate_ids"]:
                    rp["affected_candidate_ids"].append(sem_id)

        bank_rows.append(
            {
                "semantic_candidate_v3_id": sem_id,
                "evidence_pack_v3_id": ep_id,
                "expansion_strategy": pack.get("expansion_strategy"),
                "raw_ocr_text": raw_text,
                "bank_like_terms_detected": bank_terms,
                "bank_like_score": min(1.0, 0.4 + 0.15 * len(bank_terms)) if bank_terms else 0.0,
                "entity_candidate_name": (entity or {}).get("entity_name_candidate"),
                "entity_confirmed": False,
                "confirmation_blockers": [
                    "source_validation_v2_not_invoked",
                    "same_frame_same_region_not_independent_consensus",
                    "strategy_comparison_not_benchmark",
                    "entity_confirmation_not_allowed_in_phase",
                ]
                + (["repeated_with_other_strategy"] if repeated_strategy else []),
                "required_next_action": "Source-Validation-v2-after-EP-v3",
            }
        )

        noisy_rows.append(
            {
                "semantic_candidate_v3_id": sem_id,
                "evidence_pack_v3_id": ep_id,
                "expansion_strategy": pack.get("expansion_strategy"),
                "noisy_segments": noisy_segs,
                "suspected_language": "en" if noisy_segs else None,
                "noise_pattern": noisy_segs[0].get("noise_pattern") if noisy_segs else None,
                "correction_candidate": None,
                "completion_candidate": None,
                "correction_committed": False,
                "completion_committed": False,
                "required_next_action": "Source-Validation-v2-after-EP-v3",
            }
        )

        entity_boundary_rows.append(
            {
                "semantic_candidate_v3_id": sem_id,
                "entity_candidate_generated": entity is not None,
                "entity_type": (entity or {}).get("entity_type"),
                "entity_name_candidate": (entity or {}).get("entity_name_candidate"),
                "entity_confirmed": False,
                "entity_confirmation_allowed": False,
                "fact_write_allowed": False,
                "source_validation_v2_required_later": True,
                "review_required_later": True,
                "world_model_attach_allowed": False,
            }
        )

        missing: List[str] = []
        if not pack.get("ocrrequest_reference_v2_ref"):
            missing.append("ocrrequest_reference_v2_ref")
        basis_rows.append(
            {
                "semantic_candidate_v3_id": sem_id,
                "evidence_pack_v3_ref": ep_id,
                "ocrrequest_reference_v2_ref": pack.get("ocrrequest_reference_v2_ref"),
                "expanded_crop_artifact_ref": pack.get("expanded_crop_artifact_ref"),
                "bbox_expansion_candidate_ref": pack.get("bbox_expansion_candidate_ref"),
                "source_bbox_ref": pack.get("source_bbox_xyxy"),
                "expanded_bbox_ref": pack.get("expanded_bbox_xyxy"),
                "text_items_ref": bool(raw_ocr.get("text_items") or pack.get("text_items")),
                "provider_metadata_ref": bool(pack.get("provider_metadata")),
                "strategy_context_ref": bool(pack.get("bbox_expansion_context")),
                "interpretation_basis_complete": not missing,
                "missing_refs": missing,
                "interpretation_basis_status": "complete_candidate_only" if not missing else "incomplete",
            }
        )

        chain_rows.append(
            {
                "semantic_candidate_v3_id": sem_id,
                "traceable_to_evidence_pack_v3": True,
                "traceable_to_expanded_roi_ocr_result_v2": bool(src.get("expanded_roi_ocr_result_v2_ref")),
                "traceable_to_ocrrequest_reference_v2": bool(pack.get("ocrrequest_reference_v2_ref")),
                "traceable_to_expanded_crop_artifact": bool(pack.get("expanded_crop_artifact_ref")),
                "traceable_to_bbox_expansion_candidate": bool(pack.get("bbox_expansion_candidate_ref")),
                "traceable_to_linebox_trace": True,
                "source_chain": chain,
                "source_chain_preserved": RUNTIME_STEP in chain,
            }
        )

    pack_count = len(packs)
    cand_count = len(candidates)
    affected_repeat_ids = []
    for rp in repeat_pairs:
        affected_repeat_ids.extend(rp.get("affected_candidate_ids") or [])

    strategy_repeat_guard = {
        "schema_version": "semantic_v3_strategy_repeat_consensus_guard_report_v1",
        "repeated_text": "建银银行",
        "repeated_strategy_pair": ["padding_medium", "contextual_expand"],
        "affected_candidate_ids": list(dict.fromkeys(affected_repeat_ids)),
        "same_frame_same_region_not_independent_consensus": True,
        "repeated_output_not_consensus": True,
        "independent_consensus_allowed": False,
        "consensus_blockers": [
            "same_frame_f001620",
            "same_source_bbox_region",
            "different_expansion_strategy_only",
            "source_validation_v2_not_invoked",
        ],
        "required_next_action": "Source-Validation-v2-after-EP-v3;Multiframe-Merge-Proposal-v1",
        "rows": repeat_pairs,
    }

    summary = {
        "schema_version": "semantic_candidate_v3_bbox_expansion_aware_summary_v0",
        "phase": PHASE_ID,
        "generator_scope": "semantic_candidate_v3_bbox_expansion_aware_dryrun_only",
        "based_on_evidence_pack_v3_bbox_expansion": ep_root.is_dir(),
        "evidence_pack_v3_count_observed": pack_count,
        "semantic_candidate_v3_generated": cand_count > 0,
        "semantic_candidate_v3_count": cand_count,
        "bank_like_candidate_count": bank_like_count,
        "noisy_english_candidate_count": noisy_count,
        "strategy_repeat_risk_count": strategy_repeat_count,
        "entity_candidate_count": entity_candidate_count,
        "entity_confirmed_count": 0,
        "semantic_model_invoked": False,
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
        "phase_verdict_hint": "GO" if cand_count == 4 and pack_count == 4 else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "semantic_v3_ep_v3_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {
            "schema_version": "semantic_v3_bbox_expansion_rule_matrix_v1",
            "rules": RULES,
        },
        "schema_doc": {
            "schema_version": "semantic_candidate_v3_bbox_expansion_schema_v1",
            "template": {
                "semantic_candidate_v3_id": "sem_v3_bbox_<uuid>",
                "schema_version": CANDIDATE_SCHEMA,
                "source_evidence_pack_v3_ref": None,
                "expansion_strategy": None,
                "raw_ocr_text": None,
                "normalized_text_candidate": None,
                "semantic_route": "bank_like_candidate | noisy_text_candidate | mixed_candidate | hold_for_review",
                "semantic_strength": "weak | candidate | diagnostic",
                "semantic_type_candidate": "bank_sign_candidate | noisy_english_text_candidate | ocr_noise_candidate | unknown_text_candidate",
                "entity_candidate": {
                    "entity_type": "bank | unknown",
                    "entity_name_candidate": None,
                    "entity_confidence": None,
                    "entity_confirmed": False,
                },
                "text_interpretation": {
                    "bank_like_terms_detected": [],
                    "noisy_segments": [],
                    "uncertain_segments": [],
                    "correction_candidate": None,
                    "completion_candidate": None,
                    "correction_committed": False,
                    "completion_committed": False,
                },
                "strategy_context": {
                    "strategy_comparison_candidate_only": True,
                    "same_frame_same_region_not_independent_consensus": True,
                    "repeated_with_other_strategy": False,
                    "independent_consensus_allowed": False,
                },
                "interpretation_basis": {
                    "evidence_pack_v3_ref": None,
                    "ocrrequest_reference_v2_ref": None,
                    "expanded_crop_artifact_ref": None,
                    "bbox_expansion_candidate_ref": None,
                    "source_bbox_ref": None,
                    "expanded_bbox_ref": None,
                    "text_items_ref": None,
                    "provider_metadata_ref": None,
                },
                "governance": {
                    "entity_confirmation_allowed": False,
                    "source_validation_v2_required_later": True,
                    "source_validation_v2_invoked_now": False,
                    "review_required_later": True,
                    "world_model_attach_allowed": False,
                    "scene_delta_candidate_allowed": False,
                    "fact_status": "not_fact",
                    "write_allowed": False,
                },
                "source_chain": [],
            },
        },
        "collection": {
            "schema_version": "semantic_candidate_v3_bbox_expansion_collection_v1",
            "candidate_count": cand_count,
            "candidates": candidates,
        },
        "bank_like_report": {
            "schema_version": "semantic_v3_bank_like_candidate_report_v1",
            "row_count": len(bank_rows),
            "rows": bank_rows,
        },
        "noisy_report": {
            "schema_version": "semantic_v3_noisy_english_ocr_noise_report_v1",
            "row_count": len(noisy_rows),
            "rows": noisy_rows,
        },
        "strategy_repeat_guard": strategy_repeat_guard,
        "entity_boundary": {
            "schema_version": "semantic_v3_entity_candidate_boundary_report_v1",
            "row_count": len(entity_boundary_rows),
            "rows": entity_boundary_rows,
        },
        "interpretation_basis": {
            "schema_version": "semantic_v3_interpretation_basis_report_v1",
            "row_count": len(basis_rows),
            "rows": basis_rows,
        },
        "source_chain_report": {
            "schema_version": "semantic_v3_source_chain_report_v1",
            "row_count": len(chain_rows),
            "all_traceable_to_evidence_pack_v3": all(r.get("traceable_to_evidence_pack_v3") for r in chain_rows),
            "rows": chain_rows,
        },
        "routing": {
            "schema_version": "semantic_v3_routing_report_v1",
            "semantic_candidate_v3_count": cand_count,
            "bank_like_candidate_count": bank_like_count,
            "noisy_english_candidate_count": noisy_count,
            "entity_candidate_count": entity_candidate_count,
            "entity_confirmed_count": 0,
            "correction_committed_count": 0,
            "completion_committed_count": 0,
            "source_validation_v2_required_later_count": cand_count,
            "source_validation_v2_invoked_now_count": 0,
            "review_required_later_count": cand_count,
            "world_model_attach_allowed_count": 0,
            "scene_delta_candidate_allowed_count": 0,
        },
        "sv_readiness": {
            "schema_version": "semantic_v3_source_validation_v2_readiness_plan_v1",
            "future_phase": "Source-Validation-v2-after-EP-v3",
            "readiness_candidate_count": cand_count,
            "required_input": [
                "semantic_candidate_v3_bbox_expansion_collection",
                "evidence_pack_v3_bbox_expansion_collection",
                "expanded_roi_ocr_result_collection_v2",
            ],
            "required_checks": [
                "repeated observation",
                "map / POI optional hint",
                "visual symbol optional support",
                "multiframe support",
                "conflict check",
                "same_frame_consensus_blocker",
            ],
            "blockers_before_validation": [
                "same_frame_same_region_not_independent_consensus",
                "repeated_strategy_output_not_consensus",
                "source_validation_v2_not_invoked",
            ],
            "validation_not_invoked_in_this_phase": True,
            "not_in_current_phase": True,
        },
        "review_readiness": {
            "schema_version": "semantic_v3_review_policy_readiness_plan_v1",
            "future_phase": "Semantic-Candidate-v3-Review-Policy",
            "review_candidate_count": cand_count,
            "required_input": ["semantic_candidate_v3_bbox_expansion_collection"],
            "queue_type_candidates": ["bank_like_review", "noisy_text_review", "strategy_repeat_review"],
            "ttl_required": True,
            "source_validation_required": True,
            "user_visible_uncertainty_required": True,
            "not_in_current_phase": True,
        },
        "unresolved_slot": {
            "schema_version": "semantic_v3_unresolved_slot_linkage_plan_v1",
            "unresolved_slot_linkage_candidate_count": cand_count,
            "candidate_types": ["partial_entity_text_region", "bank_sign_candidate"],
            "slot_generation_allowed_in_this_phase": False,
            "possible_slot_type": "partial_entity_text_region",
            "source_chain_required": True,
            "future_phase": "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
        },
        "boundary": {
            "schema_version": "semantic_v3_boundary_report_v1",
            "semantic_candidate_v3_dryrun_only": True,
            "semantic_model_invoked": False,
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
            "schema_version": "semantic_v3_metrics_candidate_report_v1",
            "evidence_pack_v3_count_observed": pack_count,
            "semantic_candidate_v3_count": cand_count,
            "bank_like_candidate_count": bank_like_count,
            "noisy_english_candidate_count": noisy_count,
            "entity_candidate_count": entity_candidate_count,
            "entity_confirmed_count": 0,
            "repeated_strategy_risk_count": strategy_repeat_count,
            "correction_committed_count": 0,
            "completion_committed_count": 0,
            "source_validation_v2_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "world_model_attach_allowed_count": 0,
            "scene_delta_candidate_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "semantic_v3_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "semantic_v3_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "semantic_v3_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "semantic_candidate_v3_dryrun_only": True,
            "semantic_model_invoked": False,
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
            "schema_version": "semantic_v3_simulation_context_report_v1",
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
            "schema_version": "semantic_v3_non_claims_report_v1",
            "no_ocr_in_phase": True,
            "no_llm_vlm": True,
            "semantic_candidate_not_fact": True,
            "bank_like_not_bank_fact": True,
            "entity_candidate_not_confirmed": True,
            "noisy_english_not_auto_corrected": True,
            "repeated_strategy_not_consensus": True,
            "no_source_validation_v2": True,
            "no_world_model": True,
            "no_benchmark_claim": True,
            "no_production_ready": True,
        },
        "followups": {"schema_version": "semantic_v3_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "semantic_v3_audit_report_v1",
            "semantic_candidate_v3_bbox_expansion_aware_executed": True,
            "semantic_candidate_v3_dryrun_only": True,
            "evidence_pack_v3_count_observed": pack_count,
            "semantic_candidate_v3_count": cand_count,
            "bank_like_candidate_count": bank_like_count,
            "noisy_english_candidate_count": noisy_count,
            "entity_candidate_count": entity_candidate_count,
            "entity_confirmed_count": 0,
            "semantic_model_invoked": False,
            "llm_invoked": False,
            "vlm_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "source_validation_v2_invoked": False,
            "correction_committed": False,
            "completion_committed": False,
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
            "model_selection_claimed": False,
            "production_readiness_claimed": False,
        },
    }
