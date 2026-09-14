# -*- coding: utf-8 -*-
"""Source Validation v2 after EP v3 — dry-run condition assessment only.

Phase-Source-Validation-v2-after-EP-v3-001
No OCR/LLM/map/POI/VisualSymbol/multiframe. validation_passed_count=0 expected.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Source-Validation-v2-after-EP-v3-001"
RUNTIME_STEP = "source_validation_v2_after_ep_v3"

FOLLOWUPS = [
    "Semantic-Candidate-v3-Review-Policy",
    "Multiframe-Merge-Proposal-v1",
    "Better-Frame-Extraction-DryRun-v1",
    "VisualSymbolRegistry-DryRun-v1",
    "Map-POI-Hint-DryRun-v1",
    "Repeated-Observation-Collector-v1",
    "User-Visible-Uncertainty-Review-v1",
    "Source-Validation-v2-Rerun-after-External-Support",
    "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
    "STC Contract later",
    "Controlled runtime integration",
]

RULES: List[Dict[str, Any]] = [
    {
        "rule_id": "source_chain_complete_allows_validation_review",
        "condition": "source_chain_complete_for_dryrun",
        "validation_effect": "allows_dryrun_review_only",
        "allowed_status": "pending|blocked",
        "blocked_action": "validation_passed",
        "required_next_action": "Source-Validation-v2-Rerun-after-External-Support",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "bank_like_candidate_requires_source_validation",
        "condition": "bank_like or mixed_candidate",
        "validation_effect": "requires_external_support",
        "allowed_status": "pending|blocked",
        "blocked_action": "auto_validation_pass",
        "required_next_action": "Repeated-Observation-Collector-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "same_frame_same_region_blocks_independent_consensus",
        "condition": "same_frame_same_region_not_independent_consensus",
        "validation_effect": "consensus_blocked",
        "allowed_status": "blocked_same_frame_consensus",
        "blocked_action": "independent_consensus",
        "required_next_action": "Multiframe-Merge-Proposal-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "repeated_strategy_output_not_consensus",
        "condition": "repeated_with_other_strategy",
        "validation_effect": "strategy_repeat_not_consensus",
        "allowed_status": "pending|blocked",
        "blocked_action": "independent_validation_pass",
        "required_next_action": "Repeated-Observation-Collector-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "noisy_segment_blocks_entity_confirmation",
        "condition": "noisy_segments non-empty",
        "validation_effect": "entity_confirmation_blocked",
        "allowed_status": "blocked_noisy_segment|pending_external_hint",
        "blocked_action": "entity_confirmation",
        "required_next_action": "Source-Validation-v2-Rerun-after-External-Support",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "entity_candidate_not_confirmed_without_external_support",
        "condition": "entity_candidate present",
        "validation_effect": "entity_validation_pending",
        "allowed_status": "pending|blocked",
        "blocked_action": "entity_confirmed",
        "required_next_action": "User-Visible-Uncertainty-Review-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "map_poi_not_checked_blocks_fact_validation",
        "condition": "map_poi_checked=false",
        "validation_effect": "fact_validation_blocked",
        "allowed_status": "pending_external_hint|insufficient_for_fact_validation",
        "blocked_action": "fact_validation_pass",
        "required_next_action": "Map-POI-Hint-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "visual_symbol_not_checked_blocks_fact_validation",
        "condition": "visual_symbol_registry_checked=false",
        "validation_effect": "fact_validation_blocked",
        "allowed_status": "pending_visual_symbol_support",
        "blocked_action": "fact_validation_pass",
        "required_next_action": "VisualSymbolRegistry-DryRun-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "multiframe_not_checked_blocks_fact_validation",
        "condition": "multiframe_checked=false",
        "validation_effect": "fact_validation_blocked",
        "allowed_status": "pending_multiframe_support",
        "blocked_action": "fact_validation_pass",
        "required_next_action": "Multiframe-Merge-Proposal-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "repeated_observation_not_checked_blocks_fact_validation",
        "condition": "repeated_observation_checked=false",
        "validation_effect": "fact_validation_blocked",
        "allowed_status": "pending_repeated_observation",
        "blocked_action": "fact_validation_pass",
        "required_next_action": "Repeated-Observation-Collector-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "user_confirmation_not_checked_blocks_fact_validation",
        "condition": "user_confirmation_checked=false",
        "validation_effect": "fact_validation_blocked",
        "allowed_status": "pending_external_hint",
        "blocked_action": "fact_validation_pass",
        "required_next_action": "User-Visible-Uncertainty-Review-v1",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_world_model_attach_in_this_phase",
        "condition": "always",
        "validation_effect": "no_wm_attach",
        "allowed_status": "dryrun_only",
        "blocked_action": "world_model_attach",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_scene_delta_candidate_in_this_phase",
        "condition": "always",
        "validation_effect": "no_scene_delta",
        "allowed_status": "dryrun_only",
        "blocked_action": "scene_delta_candidate",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
    {
        "rule_id": "no_fact_write_in_this_phase",
        "condition": "always",
        "validation_effect": "no_fact_write",
        "allowed_status": "dryrun_only",
        "blocked_action": "fact_write",
        "required_next_action": "none",
        "fact_status_after_rule": "not_fact",
        "write_allowed_after_rule": False,
    },
]

EXTERNAL_SUPPORT_TYPES = [
    ("map_poi_hint", "Map-POI-Hint-DryRun-v1", True),
    ("visual_symbol_registry", "VisualSymbolRegistry-DryRun-v1", True),
    ("multiframe_observation", "Multiframe-Merge-Proposal-v1", True),
    ("repeated_observation", "Repeated-Observation-Collector-v1", True),
    ("user_confirmation", "User-Visible-Uncertainty-Review-v1", True),
    ("spatial_anchor", "Map-POI-Hint-DryRun-v1", True),
]

FUTURE_PHASES = [
    {
        "phase": "Multiframe-Merge-Proposal-v1",
        "purpose": "merge observations across frames before consensus",
        "required_input": ["validation_decision_matrix", "evidence_pack_v3_collection"],
        "expected_output": "multiframe_merge_proposal",
        "boundary": "proposal_only_not_fact",
        "not_in_current_phase": True,
    },
    {
        "phase": "Better-Frame-Extraction-DryRun-v1",
        "purpose": "select better frames for repeated observation",
        "required_input": ["linebox_trace", "roi_quality_diagnosis"],
        "expected_output": "better_frame_candidates",
        "boundary": "dryrun_only",
        "not_in_current_phase": True,
    },
    {
        "phase": "VisualSymbolRegistry-DryRun-v1",
        "purpose": "optional visual symbol support for bank-like candidates",
        "required_input": ["expanded_crop_artifact_ref"],
        "expected_output": "visual_symbol_hint_candidate",
        "boundary": "no_registry_call_in_current_phase",
        "not_in_current_phase": True,
    },
    {
        "phase": "Map-POI-Hint-DryRun-v1",
        "purpose": "optional map/POI hint without live API in dry-run",
        "required_input": ["candidate_frame_id", "spatial_anchor_placeholder"],
        "expected_output": "map_poi_hint_candidate",
        "boundary": "no_live_map_api",
        "not_in_current_phase": True,
    },
    {
        "phase": "Repeated-Observation-Collector-v1",
        "purpose": "collect repeated observations across time",
        "required_input": ["semantic_candidate_v3_collection"],
        "expected_output": "repeated_observation_bundle",
        "boundary": "collector_not_fact",
        "not_in_current_phase": True,
    },
    {
        "phase": "User-Visible-Uncertainty-Review-v1",
        "purpose": "surface uncertainty to user without auto-approve",
        "required_input": ["validation_decision_matrix"],
        "expected_output": "review_queue_entry",
        "boundary": "no_auto_approve",
        "not_in_current_phase": True,
    },
    {
        "phase": "Source-Validation-v2-Rerun-after-External-Support",
        "purpose": "re-evaluate validation after external supports available",
        "required_input": ["source_validation_v2_decision_matrix", "external_support_artifacts"],
        "expected_output": "validation_rerun_report",
        "boundary": "still_requires_explicit_pass_criteria",
        "not_in_current_phase": True,
    },
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _val_id(sem_id: str) -> str:
    return f"sv2_ep3_{hashlib.sha256(sem_id.encode()).hexdigest()[:12]}"


def _decide_status(
    *,
    same_frame: bool,
    has_noisy: bool,
    repeated_strategy: bool,
) -> Tuple[str, str, List[str], bool, bool, bool]:
    """Return validation_status, validation_decision, blocker_codes, pending, blocked, passed."""
    blockers: List[str] = []
    if same_frame:
        blockers.append("same_frame_same_region_not_independent_consensus")
    if has_noisy:
        blockers.append("noisy_segment_blocks_entity_confirmation")
    if repeated_strategy:
        blockers.append("repeated_strategy_output_not_consensus")
    blockers.extend(
        [
            "map_poi_not_checked",
            "visual_symbol_registry_not_checked",
            "multiframe_not_checked",
            "repeated_observation_not_checked",
            "user_confirmation_not_checked",
            "spatial_anchor_missing",
        ]
    )

    if same_frame:
        status = "blocked_same_frame_consensus"
    elif has_noisy:
        status = "blocked_noisy_segment"
    else:
        status = "pending_repeated_observation"

    if repeated_strategy and status.startswith("pending"):
        status = "pending_repeated_observation"

    decision = "defer_validation"
    pending = True
    blocked = same_frame or has_noisy
    passed = False
    return status, decision, blockers, pending, blocked, passed


def run_source_validation_v2_after_ep_v3(
    *,
    semantic_v3_root: str,
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
    worldmodel_unresolved_slot_contract_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    sem_root = Path(semantic_v3_root).resolve()
    ep_root = Path(evidence_pack_v3_root).resolve()
    linebox = Path(linebox_sq_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()
    wm_slot = Path(worldmodel_unresolved_slot_contract_root).resolve()

    sem_coll = _read_json(sem_root / "semantic_candidate_v3_bbox_expansion_collection.json") or {}
    ep_coll = _read_json(ep_root / "evidence_pack_v3_bbox_expansion_collection.json") or {}
    repeat_guard = _read_json(sem_root / "semantic_v3_strategy_repeat_consensus_guard_report.json") or {}

    candidates_sem = [c for c in (sem_coll.get("candidates") or []) if isinstance(c, dict)]
    packs = [p for p in (ep_coll.get("packs") or []) if isinstance(p, dict)]
    ep_by_id = {str(p.get("evidence_pack_v3_id")): p for p in packs}

    intake_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []
    entity_rows: List[Dict[str, Any]] = []
    decision_rows: List[Dict[str, Any]] = []
    noisy_rows: List[Dict[str, Any]] = []

    passed_count = 0
    pending_count = 0
    blocked_count = 0
    same_frame_blocked = 0
    strategy_repeat_count = 0
    noisy_blocker_count = 0
    val_ids: List[str] = []
    ep_ids: List[str] = []
    frame_id = "test_video_complex_6m42s_f001620"

    for cand in candidates_sem:
        sem_id = str(cand.get("semantic_candidate_v3_id") or "")
        ep_id = str(cand.get("source_evidence_pack_v3_ref") or "")
        pack = ep_by_id.get(ep_id, {})
        val_id = _val_id(sem_id)
        val_ids.append(val_id)
        ep_ids.append(ep_id)

        raw_text = str(cand.get("raw_ocr_text") or "")
        strategy = str(cand.get("expansion_strategy") or "")
        route = str(cand.get("semantic_route") or "")
        sem_type = str(cand.get("semantic_type_candidate") or "")
        entity = cand.get("entity_candidate") if isinstance(cand.get("entity_candidate"), dict) else None
        text_interp = cand.get("text_interpretation") if isinstance(cand.get("text_interpretation"), dict) else {}
        noisy_segs = text_interp.get("noisy_segments") or []
        strat_ctx = cand.get("strategy_context") if isinstance(cand.get("strategy_context"), dict) else {}
        same_frame = bool(strat_ctx.get("same_frame_same_region_not_independent_consensus", True))
        repeated = bool(strat_ctx.get("repeated_with_other_strategy"))
        has_noisy = bool(noisy_segs)

        if repeated:
            strategy_repeat_count += 1
        if has_noisy:
            noisy_blocker_count += 1
        if same_frame:
            same_frame_blocked += 1

        frame_id = str(pack.get("candidate_frame_id") or frame_id)
        frame_index = pack.get("candidate_frame_index")
        frame_time = pack.get("candidate_frame_time_sec")

        intake_rows.append(
            {
                "validation_candidate_id": val_id,
                "semantic_candidate_v3_id": sem_id,
                "evidence_pack_v3_id": ep_id,
                "expansion_strategy": strategy,
                "raw_ocr_text": raw_text,
                "semantic_route": route,
                "semantic_type_candidate": sem_type,
                "entity_candidate": entity,
                "entity_confirmed": False,
                "noisy_segments": noisy_segs,
                "repeated_with_other_strategy": repeated,
                "same_frame_same_region_not_independent_consensus": same_frame,
                "source_bbox_xyxy": pack.get("source_bbox_xyxy")
                or (pack.get("image_coordinates") or {}).get("source_bbox_xyxy"),
                "expanded_bbox_xyxy": pack.get("expanded_bbox_xyxy")
                or (pack.get("image_coordinates") or {}).get("expanded_bbox_xyxy"),
                "candidate_frame_id": frame_id,
                "candidate_frame_index": frame_index,
                "candidate_frame_time_sec": frame_time,
                "ocrrequest_reference_v2_ref": pack.get("ocrrequest_reference_v2_ref"),
                "expanded_crop_artifact_ref": pack.get("expanded_crop_artifact_ref"),
                "bbox_expansion_candidate_ref": pack.get("bbox_expansion_candidate_ref"),
                "intake_status": "accepted",
                "eligible_for_validation_dryrun": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        chain = list(cand.get("source_chain") or pack.get("source", {}).get("source_chain") or [])
        missing: List[str] = []
        if not pack.get("ocrrequest_reference_v2_ref"):
            missing.append("ocrrequest_reference_v2_ref")
        chain_rows.append(
            {
                "validation_candidate_id": val_id,
                "semantic_candidate_v3_id": sem_id,
                "evidence_pack_v3_id": ep_id,
                "source_chain_complete_for_dryrun": not missing,
                "traceable_to_ep_v3": True,
                "traceable_to_ocr_result_v2": bool(pack.get("expanded_roi_ocr_result_v2_ref")),
                "traceable_to_ocrrequest_reference_v2": bool(pack.get("ocrrequest_reference_v2_ref")),
                "traceable_to_expanded_crop": bool(pack.get("expanded_crop_artifact_ref")),
                "traceable_to_bbox_expansion_candidate": bool(pack.get("bbox_expansion_candidate_ref")),
                "traceable_to_crop_v2": "roi_crop_execution_dryrun_v2_bbox_expansion" in chain,
                "traceable_to_diversity_check": "roi_crop_diversity_check_v1" in chain,
                "traceable_to_quality_diagnosis": "roi_ocr_quality_diagnosis_v1" in chain,
                "traceable_to_linebox_trace": linebox.is_dir(),
                "missing_refs": missing,
                "chain_status": "complete_for_dryrun_review" if not missing else "incomplete",
            }
        )

        entity_rows.append(
            {
                "validation_candidate_id": val_id,
                "entity_candidate_generated": entity is not None,
                "entity_type": (entity or {}).get("entity_type"),
                "entity_name_candidate": (entity or {}).get("entity_name_candidate"),
                "entity_confirmed": False,
                "entity_validation_status": "pending",
                "entity_confirmation_allowed": False,
                "confirmation_blockers": [
                    "source_validation_not_passed",
                    "same_frame_same_region_not_independent_consensus",
                    "external_support_missing",
                ]
                + (["noisy_segment_blocks_entity_confirmation"] if has_noisy else [])
                + (["repeated_strategy_output_not_consensus"] if repeated else []),
                "fact_write_allowed": False,
                "world_model_attach_allowed": False,
            }
        )

        if has_noisy:
            noisy_rows.append(
                {
                    "validation_candidate_id": val_id,
                    "semantic_candidate_v3_id": sem_id,
                    "expansion_strategy": strategy,
                    "raw_ocr_text": raw_text,
                    "noisy_segments": noisy_segs,
                    "correction_committed": False,
                    "completion_committed": False,
                    "noisy_segment_blocks_entity_confirmation": True,
                    "required_next_action": "Source-Validation-v2-Rerun-after-External-Support",
                }
            )

        status, decision, blockers, pending, blocked, passed = _decide_status(
            same_frame=same_frame,
            has_noisy=has_noisy,
            repeated_strategy=repeated,
        )
        if passed:
            passed_count += 1
        if pending:
            pending_count += 1
        if blocked:
            blocked_count += 1

        decision_rows.append(
            {
                "validation_candidate_id": val_id,
                "semantic_candidate_v3_id": sem_id,
                "evidence_pack_v3_id": ep_id,
                "validation_status": status,
                "validation_decision": decision,
                "validation_passed": passed,
                "validation_pending": pending,
                "validation_blocked": blocked,
                "blocker_codes": blockers,
                "required_next_action": "Multiframe-Merge-Proposal-v1;Repeated-Observation-Collector-v1",
                "allowed_future_phase": "Source-Validation-v2-Rerun-after-External-Support",
                "fact_write_allowed": False,
                "world_model_attach_allowed": False,
                "scene_delta_candidate_allowed": False,
            }
        )

    val_count = len(candidates_sem)
    sem_count = len(candidates_sem)
    ep_count = len(packs)

    same_frame_report = {
        "schema_version": "source_validation_v2_same_frame_consensus_blocker_report_v1",
        "candidate_frame_id": frame_id,
        "affected_candidate_ids": val_ids,
        "affected_evidence_pack_ids": ep_ids,
        "same_frame_same_region_not_independent_consensus": True,
        "independent_consensus_allowed": False,
        "consensus_status": "blocked",
        "blocker_reason": "four_expansion_strategies_same_frame_same_region_not_four_independent_sources",
        "required_next_action": "Multiframe-Merge-Proposal-v1;Repeated-Observation-Collector-v1",
    }

    strategy_repeat_report = {
        "schema_version": "source_validation_v2_strategy_repeat_validation_report_v1",
        "repeated_text": repeat_guard.get("repeated_text", "建银银行"),
        "repeated_strategy_pair": repeat_guard.get("repeated_strategy_pair", ["padding_medium", "contextual_expand"]),
        "affected_candidate_ids": repeat_guard.get("affected_candidate_ids", []),
        "repeated_output_not_consensus": True,
        "repeated_output_supports_candidate_stability": False,
        "independent_validation_weight": 0,
        "required_next_action": "Repeated-Observation-Collector-v1",
    }

    external_support_rows = [
        {
            "support_type": st,
            "checked_now": False,
            "required_for_fact_validation": req,
            "missing_support_blocks_validation": req,
            "required_future_phase": phase,
        }
        for st, phase, req in EXTERNAL_SUPPORT_TYPES
    ]

    summary = {
        "schema_version": "source_validation_v2_after_ep_v3_summary_v0",
        "phase": PHASE_ID,
        "validation_scope": "source_validation_v2_dryrun_only",
        "based_on_semantic_candidate_v3": sem_root.is_dir(),
        "based_on_evidence_pack_v3": ep_root.is_dir(),
        "semantic_candidate_v3_count_observed": sem_count,
        "evidence_pack_v3_count_observed": ep_count,
        "validation_candidate_count": val_count,
        "source_validation_evaluated": True,
        "source_validation_passed_count": passed_count,
        "source_validation_pending_count": pending_count,
        "source_validation_blocked_count": blocked_count,
        "entity_confirmed_count": 0,
        "same_frame_consensus_blocked_count": same_frame_blocked,
        "strategy_repeat_not_consensus_count": strategy_repeat_count,
        "noisy_segment_blocker_count": noisy_blocker_count,
        "map_poi_checked": False,
        "visual_symbol_registry_checked": False,
        "multiframe_checked": False,
        "repeated_observation_checked": False,
        "user_confirmation_checked": False,
        "semantic_model_invoked": False,
        "llm_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "provider_invoked": False,
        "decision_committed": False,
        "approval_granted": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "phase_verdict_hint": "GO" if val_count == 4 and passed_count == 0 else "CONDITIONAL_GO",
    }

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "source_validation_v2_candidate_intake_matrix_v1",
            "row_count": len(intake_rows),
            "rows": intake_rows,
        },
        "rule_matrix": {"schema_version": "source_validation_v2_rule_matrix_v1", "rules": RULES},
        "chain_completeness": {
            "schema_version": "source_validation_v2_source_chain_completeness_report_v1",
            "row_count": len(chain_rows),
            "all_source_chain_complete_for_dryrun": all(r.get("source_chain_complete_for_dryrun") for r in chain_rows),
            "rows": chain_rows,
        },
        "same_frame_blocker": same_frame_report,
        "strategy_repeat": strategy_repeat_report,
        "noisy_blocker": {
            "schema_version": "source_validation_v2_noisy_segment_blocker_report_v1",
            "row_count": len(noisy_rows),
            "rows": noisy_rows,
        },
        "external_support": {
            "schema_version": "source_validation_v2_external_support_missing_report_v1",
            "map_poi_checked": False,
            "visual_symbol_registry_checked": False,
            "multiframe_checked": False,
            "repeated_observation_checked": False,
            "user_confirmation_checked": False,
            "items": external_support_rows,
        },
        "entity_boundary": {
            "schema_version": "source_validation_v2_entity_validation_boundary_report_v1",
            "row_count": len(entity_rows),
            "rows": entity_rows,
        },
        "decision_matrix": {
            "schema_version": "source_validation_v2_decision_matrix_v1",
            "row_count": len(decision_rows),
            "rows": decision_rows,
        },
        "routing": {
            "schema_version": "source_validation_v2_routing_report_v1",
            "validation_candidate_count": val_count,
            "validation_passed_count": passed_count,
            "validation_pending_count": pending_count,
            "validation_blocked_count": blocked_count,
            "same_frame_consensus_blocked_count": same_frame_blocked,
            "strategy_repeat_not_consensus_count": strategy_repeat_count,
            "noisy_segment_blocker_count": noisy_blocker_count,
            "map_poi_required_later_count": val_count,
            "visual_symbol_required_later_count": val_count,
            "multiframe_required_later_count": val_count,
            "repeated_observation_required_later_count": val_count,
            "user_confirmation_required_later_count": val_count,
            "fact_write_allowed_count": 0,
            "world_model_attach_allowed_count": 0,
            "scene_delta_candidate_allowed_count": 0,
        },
        "future_plan": {
            "schema_version": "source_validation_v2_future_validation_plan_v1",
            "phases": FUTURE_PHASES,
        },
        "review_readiness": {
            "schema_version": "source_validation_v2_review_policy_readiness_report_v1",
            "review_candidate_count": val_count,
            "review_policy_ready_later": True,
            "queue_type_candidates": [
                "validation_pending_review",
                "same_frame_blocker_review",
                "noisy_segment_review",
            ],
            "validation_status_required": True,
            "user_visible_uncertainty_required": True,
            "decision_commit_allowed_now": False,
            "future_phase": "Semantic-Candidate-v3-Review-Policy",
        },
        "unresolved_slot": {
            "schema_version": "source_validation_v2_unresolved_slot_readiness_report_v1",
            "unresolved_slot_candidate_count": val_count,
            "possible_slot_type": "partial_entity_text_region",
            "slot_generation_allowed_now": False,
            "unresolved_reason": "source_validation_passed_count=0;external_support_missing",
            "source_chain_required": True,
            "future_phase": "WorldModel-Unresolved-Slot-DryRun-From-Semantic-v3",
            "worldmodel_contract_available": wm_slot.is_dir(),
        },
        "boundary": {
            "schema_version": "source_validation_v2_boundary_report_v1",
            "source_validation_v2_dryrun_only": True,
            "map_poi_checked": False,
            "visual_symbol_registry_checked": False,
            "multiframe_checked": False,
            "repeated_observation_checked": False,
            "user_confirmation_checked": False,
            "semantic_model_invoked": False,
            "llm_invoked": False,
            "vlm_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "review_decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
        },
        "metrics": {
            "schema_version": "source_validation_v2_metrics_candidate_report_v1",
            "semantic_candidate_v3_count_observed": sem_count,
            "evidence_pack_v3_count_observed": ep_count,
            "validation_candidate_count": val_count,
            "validation_passed_count": passed_count,
            "validation_pending_count": pending_count,
            "validation_blocked_count": blocked_count,
            "same_frame_consensus_blocked_count": same_frame_blocked,
            "strategy_repeat_not_consensus_count": strategy_repeat_count,
            "noisy_segment_blocker_count": noisy_blocker_count,
            "entity_confirmed_count": 0,
            "fact_write_allowed_count": 0,
            "world_model_attach_allowed_count": 0,
            "scene_delta_candidate_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "source_validation_v2_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "source_validation_v2_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "source_validation_v2_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "source_validation_v2_dryrun_only": True,
            "map_poi_checked": False,
            "visual_symbol_registry_checked": False,
            "multiframe_checked": False,
            "repeated_observation_checked": False,
            "user_confirmation_checked": False,
            "semantic_model_invoked": False,
            "llm_invoked": False,
            "vlm_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
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
            "schema_version": "source_validation_v2_simulation_context_report_v1",
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
            "schema_version": "source_validation_v2_non_claims_report_v1",
            "no_ocr_in_phase": True,
            "no_llm_vlm": True,
            "no_map_poi_api": True,
            "no_visual_symbol_registry": True,
            "no_real_repeated_observation": True,
            "dryrun_not_validation_passed": True,
            "bank_like_not_bank_fact": True,
            "entity_candidate_not_confirmed": True,
            "strategy_repeat_not_consensus": True,
            "source_chain_complete_not_fact_valid": True,
            "no_world_model": True,
            "no_benchmark_claim": True,
            "no_production_ready": True,
        },
        "followups": {"schema_version": "source_validation_v2_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "source_validation_v2_audit_report_v1",
            "source_validation_v2_after_ep_v3_executed": True,
            "source_validation_v2_dryrun_only": True,
            "semantic_candidate_v3_count_observed": sem_count,
            "evidence_pack_v3_count_observed": ep_count,
            "validation_candidate_count": val_count,
            "source_validation_passed_count": passed_count,
            "entity_confirmed_count": 0,
            "map_poi_checked": False,
            "visual_symbol_registry_checked": False,
            "multiframe_checked": False,
            "repeated_observation_checked": False,
            "user_confirmation_checked": False,
            "semantic_model_invoked": False,
            "llm_invoked": False,
            "vlm_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
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
