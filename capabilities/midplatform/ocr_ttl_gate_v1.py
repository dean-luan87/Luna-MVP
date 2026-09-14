# -*- coding: utf-8 -*-
"""OCR TTL Gate v1 — dry-run evaluation for ttl_review_queue items only.

Phase-OCR-TTL-Gate-v1-001
No decision commit, no approval, no fact/WM/SceneDelta writes.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCR-TTL-Gate-v1-001"
GATE_STEP = "ocr_ttl_gate_v1"

TTL_SEMANTIC_TYPES = {"poster_promo_text", "price_discount_text", "temporal_notice_text"}

PATTERN_DEFS: List[Tuple[str, str]] = [
    ("discount_pattern", r"折|优惠|特价|满减"),
    ("price_pattern", r"\d+[\.\d]*\s*元|￥|¥"),
    ("date_pattern", r"\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?|\d{1,2}月\d{1,2}日"),
    ("date_range_pattern", r"\d{1,2}月\d{1,2}日\s*[-至~]\s*\d{1,2}月\d{1,2}日"),
    ("event_period_pattern", r"活动期间|限时|截止|有效期"),
    ("opening_hours_pattern", r"\d{1,2}:\d{2}\s*[-–]\s*\d{1,2}:\d{2}|营业时间"),
    ("limited_time_claim", r"限时|仅限|最后\d+天"),
    ("commercial_promo_claim", r"促销|活动|特惠|爆款|包邮"),
]

VALIDITY_END_RE = re.compile(
    r"(?:截止|至|有效期至|活动至)\s*(\d{4}[-/年]?\d{1,2}[-/月]?\d{1,2}日?)",
    re.IGNORECASE,
)
VALIDITY_START_RE = re.compile(
    r"(?:自|从)\s*(\d{4}[-/年]?\d{1,2}[-/月]?\d{1,2}日?)",
    re.IGNORECASE,
)

POLICY_REQUIREMENTS = [
    ("explicit_validity_period", True, True, "commercial_temporal_text_requires_explicit_validity"),
    ("source_validation", True, True, "source_must_be_validated_before_fact"),
    ("stale_check", True, True, "expired_content_must_not_promote_to_fact"),
    ("conflict_check", True, False, "conflicting_promo_claims_need_review"),
    ("review", True, True, "human_or_policy_review_before_fact"),
    ("rollback_policy", True, False, "rollback_on_ttl_violation_later"),
    ("expiry_policy", True, True, "expiry_handling_required_for_promo"),
    ("user_visible_uncertainty", True, True, "user_must_see_ttl_uncertainty_when_unverified"),
    ("no_world_model_write_before_ttl", True, True, "world_model_blocked_until_ttl_satisfied"),
    ("no_scene_delta_before_ttl", True, True, "scene_delta_blocked_until_ttl_satisfied"),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _detect_patterns(raw: str) -> List[str]:
    found = []
    for name, pat in PATTERN_DEFS:
        if re.search(pat, raw or ""):
            found.append(name)
    return found


def _detect_validity(raw: str) -> Tuple[bool, Optional[str], Optional[str]]:
    end_m = VALIDITY_END_RE.search(raw or "")
    start_m = VALIDITY_START_RE.search(raw or "")
    end_c = end_m.group(1) if end_m else None
    start_c = start_m.group(1) if start_m else None
    explicit = bool(end_c or start_c or re.search(r"有效期|截止|至\s*\d", raw or ""))
    return explicit, start_c, end_c


def _build_semantic_index(semantic_root: Path) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    gated = _read_json(semantic_root / "ocr_semantic_candidate_v1_gated_ocr_collection.json") or {}
    for c in gated.get("candidates") or []:
        if isinstance(c, dict) and c.get("semantic_candidate_id"):
            idx[str(c["semantic_candidate_id"])] = c
    return idx


def _load_ttl_queue_items(runtime_root: Path) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    intake = _read_json(runtime_root / "ocr_review_queue_runtime_intake_report.json") or {}
    all_rows = [r for r in (intake.get("rows") or []) if isinstance(r, dict)]
    ttl_rows = [r for r in all_rows if r.get("queue_type") == "ttl_review_queue"]
    dist = (intake.get("queue_type_distribution") or {}).get("ttl_review_queue")
    mismatch = None
    if dist is not None and dist != len(ttl_rows):
        mismatch = f"upstream_ttl_count={dist},intake_ttl_rows={len(ttl_rows)}"
    return ttl_rows, mismatch


def _evaluate_ttl_item(
    intake_row: Dict[str, Any],
    semantic: Dict[str, Any],
) -> Dict[str, Any]:
    raw = str(semantic.get("raw_ocr_text") or "")
    st = str(semantic.get("semantic_type_candidate") or "poster_promo_text")
    ib = semantic.get("interpretation_basis") or {}

    patterns = _detect_patterns(raw)
    explicit, v_start, v_end = _detect_validity(raw)
    commercial = bool(
        re.search(r"折|优惠|特价|元|促销|活动|海报|治愈|自愈", raw)
        or st in TTL_SEMANTIC_TYPES
    )
    temporal = bool(re.search(r"\d{4}|月|日|有效期|截止", raw) or st == "temporal_notice_text")
    price_disc = bool(re.search(r"\d+[\.\d]*\s*元|折|优惠|特价", raw) or st == "price_discount_text")

    ttl_required = st in TTL_SEMANTIC_TYPES or commercial or price_disc or temporal
    hold_reasons: List[str] = []
    if ttl_required:
        hold_reasons.append("commercial_or_temporal_ocr_requires_ttl_gate")
    if not explicit:
        hold_reasons.append("missing_explicit_validity_period")
    else:
        hold_reasons.append("explicit_validity_detected_but_not_verified")
    hold_reasons.append("source_validation_not_satisfied")
    hold_reasons.append("ttl_policy_satisfied_false_in_dryrun_phase")

    if not explicit:
        gate_status = "hold_for_ttl_policy"
        next_action = "collect_validity_period_or_defer"
    elif explicit:
        gate_status = "hold_for_source_validation"
        next_action = "source_validation_dryrun_later"
    else:
        gate_status = "hold_for_review"
        next_action = "review_policy_later"

    return {
        "ttl_eval_id": f"ttl_eval_{intake_row.get('runtime_queue_item_id', '')}",
        "runtime_queue_item_id": intake_row.get("runtime_queue_item_id"),
        "raw_ocr_text": raw,
        "semantic_type_candidate": st,
        "commercial_claim_detected": commercial,
        "temporal_text_detected": temporal,
        "price_or_discount_detected": price_disc,
        "explicit_validity_period_detected": explicit,
        "validity_start_candidate": v_start,
        "validity_end_candidate": v_end,
        "ttl_required": ttl_required,
        "ttl_policy_satisfied": False,
        "ttl_gate_status": gate_status,
        "hold_reasons": hold_reasons,
        "required_next_action": next_action,
        "source_validation_required": True,
        "review_required": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "ocr_request_ref": semantic.get("source_ocr_request_ref"),
        "evidence_pack_ref": ib.get("evidence_pack_ref"),
        "source_quality_grade": semantic.get("source_quality_grade"),
        "readability_grade": semantic.get("readability_grade"),
    }


def run_ocr_ttl_gate_v1(
    *,
    output_root: str,
    review_queue_runtime_root: str,
    review_policy_v1_root: str,
    semantic_v1_root: str,
    adapter_v1_root: str,
    mixed_batch_v2_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    errs: List[str] = []
    runtime = Path(review_queue_runtime_root).resolve()
    policy = Path(review_policy_v1_root).resolve()
    semantic = Path(semantic_v1_root).resolve()
    adapter = Path(adapter_v1_root).resolve()
    v2 = Path(mixed_batch_v2_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    if not runtime.is_dir():
        errs.append("missing_root:review_queue_runtime")

    ttl_intake_rows, mismatch = _load_ttl_queue_items(runtime)
    semantic_idx = _build_semantic_index(semantic)

    policy_ttl = (_read_json(policy / "ocr_semantic_review_policy_v1_queue_candidate_matrix.json") or {})
    policy_ttl_count = sum(
        1 for r in (policy_ttl.get("rows") or []) if isinstance(r, dict) and r.get("queue_type") == "ttl_review_queue"
    )

    intake_matrix_rows: List[Dict[str, Any]] = []
    eval_rows: List[Dict[str, Any]] = []
    pattern_rows: List[Dict[str, Any]] = []
    decision_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []

    for row in ttl_intake_rows:
        sid = str(row.get("source_semantic_item_id") or "")
        sem = semantic_idx.get(sid)
        if not sem:
            errs.append(f"missing_semantic:{sid}")
            continue

        ib = sem.get("interpretation_basis") or {}
        intake_matrix_rows.append(
            {
                "runtime_queue_item_id": row.get("runtime_queue_item_id"),
                "source_review_queue_candidate_id": row.get("source_review_queue_candidate_id"),
                "source_semantic_item_id": sid,
                "semantic_type_candidate": sem.get("semantic_type_candidate"),
                "raw_ocr_text": sem.get("raw_ocr_text"),
                "evidence_tier": row.get("evidence_tier"),
                "source_quality_grade": sem.get("source_quality_grade"),
                "readability_grade": sem.get("readability_grade"),
                "ocr_request_ref": sem.get("source_ocr_request_ref"),
                "evidence_pack_ref": ib.get("evidence_pack_ref"),
                "intake_status": "accepted",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        ev = _evaluate_ttl_item(row, sem)
        eval_rows.append(ev)

        patterns = _detect_patterns(str(sem.get("raw_ocr_text") or ""))
        pattern_rows.append(
            {
                "item_id": ev["ttl_eval_id"],
                "raw_ocr_text": sem.get("raw_ocr_text"),
                "detected_patterns": patterns,
                "pattern_confidence": "heuristic_low" if patterns else "none",
                "pattern_detection_status": "detected_not_confirmed" if patterns else "no_pattern",
                "pattern_detection_not_fact": True,
            }
        )

        gate_decision = ev["ttl_gate_status"].replace("hold_for_", "hold_for_")
        if gate_decision == "hold_for_ttl_policy":
            ttl_gate_decision = "hold_for_ttl_policy"
        elif gate_decision == "hold_for_source_validation":
            ttl_gate_decision = "hold_for_source_validation"
        else:
            ttl_gate_decision = "hold_for_review"

        decision_rows.append(
            {
                "runtime_queue_item_id": row.get("runtime_queue_item_id"),
                "ttl_gate_decision": ttl_gate_decision,
                "decision_status": "not_committed",
                "approval_status": "not_approved",
                "allowed_next_phase": "source_validation_dryrun_or_review_decision_dryrun",
                "blocked_actions": [
                    "approve",
                    "commit_decision",
                    "fact_write",
                    "world_model_attach",
                    "scene_delta_candidate",
                    "auto_approve",
                ],
                "world_model_write_allowed": False,
                "scene_delta_candidate_allowed": False,
                "fact_write_allowed": False,
            }
        )

        chain = list(ib.get("source_chain") or [])
        if GATE_STEP not in chain:
            chain.append(GATE_STEP)
        chain_rows.append(
            {
                "runtime_queue_item_id": row.get("runtime_queue_item_id"),
                "source_review_queue_candidate_id": row.get("source_review_queue_candidate_id"),
                "source_semantic_item_id": sid,
                "traceable_to_review_queue_runtime": True,
                "traceable_to_semantic_v1": True,
                "traceable_to_evidence_pack_v1": bool((ib.get("evidence_pack_ref") or {}).get("evidence_id")),
                "traceable_to_ocr_request": bool((sem.get("source_ocr_request_ref") or {}).get("request_id")),
                "input_candidate_ref": ib.get("input_candidate_ref"),
                "source_chain": chain,
                "source_chain_preserved": GATE_STEP in chain,
            }
        )

    status_counts = Counter(e.get("ttl_gate_status") for e in eval_rows)
    hold_ttl = status_counts.get("hold_for_ttl_policy", 0)
    hold_sv = status_counts.get("hold_for_source_validation", 0)
    hold_rev = status_counts.get("hold_for_review", 0)
    explicit_count = sum(1 for e in eval_rows if e.get("explicit_validity_period_detected"))

    policy_req_matrix = {
        "schema_version": "ocr_ttl_gate_v1_policy_requirement_matrix_v0",
        "requirements": [
            {
                "requirement_id": rid,
                "required_before_fact": req,
                "satisfied_in_this_phase": False,
                "blocking": blocking,
                "reason": reason,
            }
            for rid, req, blocking, reason in POLICY_REQUIREMENTS
        ],
    }

    boundary = {
        "schema_version": "ocr_ttl_gate_v1_boundary_report_v0",
        "ttl_gate_dryrun_only": True,
        "ttl_gate_does_not_commit_decision": True,
        "approval_granted_count": 0,
        "fact_review_generated": False,
        "world_model_attach_allowed": False,
        "scene_delta_candidate_allowed": False,
        "world_model_write_allowed": False,
        "navigation_decision_allowed": False,
    }

    metrics = {
        "schema_version": "ocr_ttl_gate_v1_metrics_candidate_report_v0",
        "ttl_queue_item_count": len(ttl_intake_rows),
        "ttl_evaluated_count": len(eval_rows),
        "ttl_required_count": sum(1 for e in eval_rows if e.get("ttl_required")),
        "explicit_validity_detected_count": explicit_count,
        "hold_for_ttl_policy_count": hold_ttl,
        "hold_for_source_validation_count": hold_sv,
        "hold_for_review_count": hold_rev,
        "ttl_gate_passed_count": 0,
        "approval_granted_count": 0,
        "fact_write_allowed_count": 0,
        "no_write_boundary_pass_rate": 1.0,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    benchmark_link = {
        "schema_version": "ocr_ttl_gate_v1_benchmark_link_report_v0",
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "current_phase_collects_t2": False,
        "ground_truth_available": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": "ocr_ttl_gate_v1_system_health_link_report_v0",
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    no_write = {
        "schema_version": "ocr_ttl_gate_v1_no_write_boundary_report_v0",
        "boundary_ok": True,
        "violations": [],
        "ttl_gate_dryrun_only": True,
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
    }

    sim_sm = _read_json(sim / "simulation_summary.json") or {}
    sim_report = {
        "schema_version": "ocr_ttl_gate_v1_simulation_context_report_v0",
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": "ocr_ttl_gate_v1_non_claims_report_v0",
        "no_ocr_execution": True,
        "no_llm_vlm": True,
        "no_review_decision_commit": True,
        "no_candidate_approval": True,
        "no_fact_review": True,
        "no_world_model_write": True,
        "no_scene_delta": True,
        "not_commercial_validity_claim": True,
        "not_promo_truth_claim": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": "ocr_ttl_gate_v1_open_followups_v0",
        "items": [
            "TTL Policy Runtime v1",
            "Source Validation DryRun",
            "Stale / Expiry Check",
            "Conflict Check",
            "User-visible uncertainty phrase policy",
            "Review Decision DryRun",
            "Scene Delta candidate later",
            "WorldModel attach later",
            "Benchmark T2 collector",
            "Controlled runtime integration",
        ],
    }

    audit = {
        "schema_version": "ocr_ttl_gate_v1_audit_report_v0",
        "ocr_ttl_gate_v1_executed": True,
        "ttl_gate_dryrun_only": True,
        "ttl_gate_evaluated": len(eval_rows) > 0,
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
    }

    summary = {
        "schema_version": "ocr_ttl_gate_v1_summary_v0",
        "phase": PHASE_ID,
        "gate_scope": "ttl_gate_dryrun_only",
        "based_on_review_queue_runtime": runtime.is_dir(),
        "ttl_queue_item_count": len(ttl_intake_rows),
        "ttl_gate_evaluated": len(eval_rows) == len(ttl_intake_rows) and len(ttl_intake_rows) > 0,
        "ttl_gate_passed_count": 0,
        "ttl_gate_hold_count": len(eval_rows),
        "ttl_gate_reject_count": 0,
        "decision_committed": False,
        "approval_granted": False,
        "auto_approve_invoked": False,
        "fact_review_generated": False,
        "world_model_attach_executed": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "policy_ttl_queue_count": policy_ttl_count,
        "upstream_mismatch_reason": mismatch,
        "phase_verdict_hint": "GO" if not errs and len(eval_rows) == len(ttl_intake_rows) else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs

    return {
        "summary": summary,
        "intake_matrix": {
            "schema_version": "ocr_ttl_gate_v1_queue_intake_matrix_v0",
            "ttl_only": True,
            "input_ttl_candidate_count": len(ttl_intake_rows),
            "policy_ttl_queue_count": policy_ttl_count,
            "upstream_mismatch_reason": mismatch,
            "rows": intake_matrix_rows,
        },
        "evaluation_matrix": {
            "schema_version": "ocr_ttl_gate_v1_evaluation_matrix_v0",
            "row_count": len(eval_rows),
            "all_ttl_policy_satisfied_false": all(e.get("ttl_policy_satisfied") is False for e in eval_rows),
            "rows": eval_rows,
        },
        "text_pattern": {
            "schema_version": "ocr_ttl_gate_v1_text_pattern_report_v0",
            "row_count": len(pattern_rows),
            "rows": pattern_rows,
        },
        "policy_requirement": policy_req_matrix,
        "decision_matrix": {
            "schema_version": "ocr_ttl_gate_v1_decision_matrix_v0",
            "row_count": len(decision_rows),
            "all_not_approved": all(d.get("approval_status") == "not_approved" for d in decision_rows),
            "rows": decision_rows,
        },
        "source_chain": {
            "schema_version": "ocr_ttl_gate_v1_source_chain_report_v0",
            "row_count": len(chain_rows),
            "all_traceable_to_semantic_v1": all(r.get("traceable_to_semantic_v1") for r in chain_rows),
            "all_traceable_to_review_queue_runtime": all(r.get("traceable_to_review_queue_runtime") for r in chain_rows),
            "rows": chain_rows,
        },
        "boundary": boundary,
        "metrics": metrics,
        "benchmark_link": benchmark_link,
        "health_link": health_link,
        "no_write": no_write,
        "sim_report": sim_report,
        "non_claims": non_claims,
        "followups": followups,
        "audit": audit,
        "errs": errs,
    }
