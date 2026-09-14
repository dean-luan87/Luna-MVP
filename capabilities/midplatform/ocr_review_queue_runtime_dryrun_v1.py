# -*- coding: utf-8 -*-
"""OCR Review Queue Runtime DryRun v1 — enqueue/sort/transition/dequeue simulation.

Phase-OCR-Review-Queue-Runtime-DryRun-v1-001
Consumes review_queue_candidate from Review Policy v1 only. No decisions committed.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCR-Review-Queue-Runtime-DryRun-v1-001"
RUNTIME_STEP = "ocr_review_queue_runtime_dryrun_v1"

PRIORITY_BY_QUEUE: Dict[str, str] = {
    "ttl_review_queue": "P1",
    "source_validation_queue": "P1",
    "visual_symbol_registry_queue": "P2",
    "roi_retry_queue": "P2",
    "better_source_queue": "P3",
    "unresolved_slot_later_queue": "P3",
    "hold_for_review_queue": "P2",
}

HANDLER_BY_QUEUE: Dict[str, str] = {
    "ttl_review_queue": "ttl_review_dryrun_handler",
    "source_validation_queue": "source_validation_dryrun_handler",
    "visual_symbol_registry_queue": "visual_symbol_registry_dryrun_handler",
    "roi_retry_queue": "roi_retry_dryrun_handler",
    "better_source_queue": "better_source_dryrun_handler",
    "unresolved_slot_later_queue": "unresolved_slot_later_dryrun_handler",
    "hold_for_review_queue": "hold_for_review_dryrun_handler",
}

DRYRUN_RESULT_BY_QUEUE: Dict[str, str] = {
    "ttl_review_queue": "ttl_review_required_ttl_not_satisfied",
    "source_validation_queue": "validation_required_validation_not_satisfied",
    "visual_symbol_registry_queue": "registry_lookup_required_no_registry_query",
    "roi_retry_queue": "roi_retry_plan_required_not_executed",
    "better_source_queue": "better_source_required",
    "unresolved_slot_later_queue": "unresolved_slot_later_no_slot_generated",
    "hold_for_review_queue": "held_pending_future_review_phase",
}

PLANNED_ACTION_BY_QUEUE: Dict[str, str] = {
    "ttl_review_queue": "ttl_gate_v1_later",
    "source_validation_queue": "source_validation_dryrun_later",
    "visual_symbol_registry_queue": "visual_symbol_registry_later",
    "roi_retry_queue": "roi_proposal_later",
    "better_source_queue": "better_source_or_roi_later",
    "unresolved_slot_later_queue": "unresolved_slot_dryrun_later",
    "hold_for_review_queue": "human_or_runtime_review_later",
}

FORBIDDEN_STATES = {
    "approved",
    "committed",
    "written_to_fact",
    "attached_to_world_model",
    "scene_delta_generated",
}

CLASSIFICATION_ENTRIES = [
    {
        "queue_type": "ttl_review_queue",
        "default_priority": "P1",
        "required_handler": "ttl_review_dryrun_handler",
        "allowed_runtime_action": ["enqueue", "sort", "dryrun_evaluate", "dequeue_simulate"],
        "forbidden_runtime_action": ["commit_decision", "approve", "write_fact"],
    },
    {
        "queue_type": "source_validation_queue",
        "default_priority": "P1",
        "required_handler": "source_validation_dryrun_handler",
        "allowed_runtime_action": ["enqueue", "sort", "dryrun_evaluate", "dequeue_simulate"],
        "forbidden_runtime_action": ["commit_decision", "approve", "write_fact"],
    },
    {
        "queue_type": "visual_symbol_registry_queue",
        "default_priority": "P2",
        "required_handler": "visual_symbol_registry_dryrun_handler",
        "allowed_runtime_action": ["enqueue", "sort", "dryrun_evaluate", "dequeue_simulate"],
        "forbidden_runtime_action": ["commit_decision", "approve", "brand_fact_write"],
    },
    {
        "queue_type": "roi_retry_queue",
        "default_priority": "P2",
        "required_handler": "roi_retry_dryrun_handler",
        "allowed_runtime_action": ["enqueue", "sort", "dryrun_evaluate", "dequeue_simulate"],
        "forbidden_runtime_action": ["commit_decision", "approve", "execute_roi_crop"],
    },
    {
        "queue_type": "better_source_queue",
        "default_priority": "P3",
        "required_handler": "better_source_dryrun_handler",
        "allowed_runtime_action": ["enqueue", "sort", "dryrun_evaluate", "dequeue_simulate"],
        "forbidden_runtime_action": ["commit_decision", "approve", "strong_semantic"],
    },
    {
        "queue_type": "unresolved_slot_later_queue",
        "default_priority": "P3",
        "required_handler": "unresolved_slot_later_dryrun_handler",
        "allowed_runtime_action": ["enqueue", "sort", "dryrun_evaluate", "dequeue_simulate"],
        "forbidden_runtime_action": ["commit_decision", "approve", "generate_real_slot"],
    },
    {
        "queue_type": "hold_for_review_queue",
        "default_priority": "P2",
        "required_handler": "hold_for_review_dryrun_handler",
        "allowed_runtime_action": ["enqueue", "sort", "dryrun_evaluate", "dequeue_simulate"],
        "forbidden_runtime_action": ["commit_decision", "approve", "auto_approve"],
    },
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _runtime_item_id(candidate_id: str) -> str:
    h = hashlib.sha256(candidate_id.encode()).hexdigest()[:12]
    return f"rq_rt_{h}"


def _final_status(queue_type: str) -> str:
    if queue_type in ("ttl_review_queue", "visual_symbol_registry_queue"):
        return "held"
    if queue_type in ("roi_retry_queue", "better_source_queue", "unresolved_slot_later_queue"):
        return "deferred"
    if queue_type == "hold_for_review_queue":
        return "held"
    return "closed_no_decision"


def _build_semantic_index(semantic_root: Path) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    gated = _read_json(semantic_root / "ocr_semantic_candidate_v1_gated_ocr_collection.json") or {}
    for c in gated.get("candidates") or []:
        if isinstance(c, dict) and c.get("semantic_candidate_id"):
            idx[str(c["semantic_candidate_id"])] = {"type": "gated", "ref": c}
    scan = _read_json(semantic_root / "ocr_semantic_candidate_v1_scan_observation_hint_report.json") or {}
    for h in scan.get("hints") or []:
        if isinstance(h, dict) and h.get("scan_hint_id"):
            idx[str(h["scan_hint_id"])] = {"type": "scan_hint", "ref": h}
    visual = _read_json(semantic_root / "ocr_semantic_candidate_v1_visual_symbol_route_report.json") or {}
    for v in visual.get("routes") or []:
        if isinstance(v, dict) and v.get("visual_route_id"):
            idx[str(v["visual_route_id"])] = {"type": "visual_route", "ref": v}
    blocked = _read_json(semantic_root / "ocr_semantic_candidate_v1_sq_e_blocked_report.json") or {}
    for b in blocked.get("items") or []:
        if isinstance(b, dict) and b.get("blocked_item_id"):
            idx[str(b["blocked_item_id"])] = {"type": "sq_e_blocked", "ref": b}
    return idx


def run_ocr_review_queue_runtime_dryrun_v1(
    *,
    output_root: str,
    review_policy_v1_root: str,
    semantic_v1_root: str,
    adapter_v1_root: str,
    mixed_batch_v2_root: str,
    worldmodel_unresolved_slot_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    errs: List[str] = []
    policy = Path(review_policy_v1_root).resolve()
    semantic = Path(semantic_v1_root).resolve()
    adapter = Path(adapter_v1_root).resolve()
    v2 = Path(mixed_batch_v2_root).resolve()
    wm_slot = Path(worldmodel_unresolved_slot_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    if not policy.is_dir():
        errs.append("missing_root:review_policy_v1")

    queue_doc = _read_json(policy / "ocr_semantic_review_policy_v1_queue_candidate_matrix.json") or {}
    candidates = [r for r in (queue_doc.get("rows") or []) if isinstance(r, dict)]
    expected_count = queue_doc.get("candidate_count", len(candidates))

    semantic_idx = _build_semantic_index(semantic)
    gated_packs = {
        p.get("evidence_id"): p
        for p in ((_read_json(adapter / "ocr_evidence_pack_v1_gated_collection.json") or {}).get("packs") or [])
        if isinstance(p, dict)
    }

    # duplicate groups: same source_semantic_item_id
    by_source: Dict[str, List[str]] = defaultdict(list)
    for c in candidates:
        sid = str(c.get("source_semantic_item_id") or "")
        by_source[sid].append(str(c.get("review_queue_candidate_id") or ""))
    duplicate_groups = {sid: ids for sid, ids in by_source.items() if len(ids) > 1}

    intake_rows: List[Dict[str, Any]] = []
    runtime_items: List[Dict[str, Any]] = []

    for i, cand in enumerate(candidates):
        cid = str(cand.get("review_queue_candidate_id") or "")
        sid = str(cand.get("source_semantic_item_id") or "")
        qtype = str(cand.get("queue_type") or "")
        rt_id = _runtime_item_id(cid)
        dup_gid = None
        if sid in duplicate_groups and len(duplicate_groups[sid]) > 1:
            dup_gid = f"dup_grp_{hashlib.sha256(sid.encode()).hexdigest()[:8]}"

        missing = []
        for field in ("review_queue_candidate_id", "queue_type", "source_semantic_item_id"):
            if not cand.get(field):
                missing.append(field)

        accepted = len(missing) == 0
        intake_rows.append(
            {
                "source_review_queue_candidate_id": cid,
                "queue_type": qtype,
                "source_semantic_item_id": sid,
                "evidence_tier": cand.get("evidence_tier"),
                "semantic_route": cand.get("semantic_route"),
                "required_gates": cand.get("required_gates") or [],
                "approval_status": cand.get("approval_status"),
                "accepted_into_runtime_queue": accepted,
                "rejection_reason": None if accepted else f"missing_fields:{missing}",
                "runtime_queue_item_id": rt_id if accepted else None,
                "duplicate_group_id": dup_gid,
            }
        )

        if not accepted:
            continue

        sem_entry = semantic_idx.get(sid, {})
        chain = ["review_policy_v1_queue_candidate", RUNTIME_STEP]
        if sem_entry:
            chain.insert(0, f"semantic_v1_{sem_entry.get('type')}")

        priority = PRIORITY_BY_QUEUE.get(qtype, "P3")
        item = {
            "runtime_queue_item_id": rt_id,
            "schema_version": "ocr_review_queue_runtime_item_v1",
            "source_review_queue_candidate_id": cid,
            "source_semantic_item_id": sid,
            "queue_type": qtype,
            "priority": priority,
            "runtime_status": "queued",
            "required_gates": cand.get("required_gates") or [],
            "blocked_actions": list(cand.get("blocked_actions") or []),
            "planned_next_action": PLANNED_ACTION_BY_QUEUE.get(qtype),
            "decision_status": "not_committed",
            "approval_status": "not_approved",
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": chain,
            "duplicate_group_id": dup_gid,
            "original_order": i,
        }
        runtime_items.append(item)

    # classification matrix with counts
    qtype_counts = Counter(c.get("queue_type") for c in candidates)
    classification = {
        "schema_version": "ocr_review_queue_runtime_classification_matrix_v0",
        "categories": [],
    }
    for entry in CLASSIFICATION_ENTRIES:
        qt = entry["queue_type"]
        classification["categories"].append(
            {
                **entry,
                "item_count": qtype_counts.get(qt, 0),
                "can_commit_decision": False,
                "can_approve": False,
                "can_write_fact": False,
            }
        )

    priority_policy = {
        "schema_version": "ocr_review_queue_runtime_priority_policy_v1",
        "rules": [
            {
                "priority_rule_id": "p1_ttl_and_validation",
                "applies_to_queue_type": ["ttl_review_queue", "source_validation_queue"],
                "priority": "P1",
                "reason": "commercial_temporal_or_entity_validation_before_downstream",
                "escalation_allowed": True,
                "escalation_requires_human_or_future_runtime": True,
                "auto_escalation_committed": False,
            },
            {
                "priority_rule_id": "p2_visual_and_roi",
                "applies_to_queue_type": ["visual_symbol_registry_queue", "roi_retry_queue", "hold_for_review_queue"],
                "priority": "P2",
                "reason": "registry_or_roi_before_better_source_backlog",
                "escalation_allowed": True,
                "escalation_requires_human_or_future_runtime": True,
                "auto_escalation_committed": False,
            },
            {
                "priority_rule_id": "p3_better_source_and_unresolved",
                "applies_to_queue_type": ["better_source_queue", "unresolved_slot_later_queue"],
                "priority": "P3",
                "reason": "deferred_observation_fill_and_source_improvement",
                "escalation_allowed": False,
                "escalation_requires_human_or_future_runtime": True,
                "auto_escalation_committed": False,
            },
        ],
    }

    def _prio_rank(p: str) -> int:
        return {"P0": 0, "P1": 1, "P2": 2, "P3": 3}.get(p, 9)

    sorted_items = sorted(runtime_items, key=lambda x: (_prio_rank(x["priority"]), x["original_order"]))
    sort_rows = []
    for so, item in enumerate(sorted_items):
        sort_rows.append(
            {
                "runtime_queue_item_id": item["runtime_queue_item_id"],
                "queue_type": item["queue_type"],
                "original_order": item["original_order"],
                "assigned_priority": item["priority"],
                "sorted_order": so,
                "priority_reason": f"policy_{item['queue_type']}_{item['priority']}",
                "escalation_status": "not_escalated",
                "decision_committed": False,
                "approval_status": "not_approved",
            }
        )

    state_plan = {
        "schema_version": "ocr_review_queue_runtime_state_transition_plan_v0",
        "states": [
            {
                "state": "queued",
                "entry_condition": "accepted_into_runtime_queue",
                "allowed_transition": ["in_review_dryrun"],
                "forbidden_transition": list(FORBIDDEN_STATES),
                "decision_committed_allowed": False,
                "approval_allowed": False,
                "write_allowed": False,
            },
            {
                "state": "in_review_dryrun",
                "entry_condition": "dequeue_or_process_simulation_started",
                "allowed_transition": ["dryrun_evaluated"],
                "forbidden_transition": list(FORBIDDEN_STATES),
                "decision_committed_allowed": False,
                "approval_allowed": False,
                "write_allowed": False,
            },
            {
                "state": "dryrun_evaluated",
                "entry_condition": "handler_dryrun_completed",
                "allowed_transition": ["held", "deferred", "closed_no_decision", "rejected_from_runtime"],
                "forbidden_transition": list(FORBIDDEN_STATES),
                "decision_committed_allowed": False,
                "approval_allowed": False,
                "write_allowed": False,
            },
            {
                "state": "held",
                "entry_condition": "ttl_or_registry_pending",
                "allowed_transition": ["closed_no_decision"],
                "forbidden_transition": list(FORBIDDEN_STATES),
                "decision_committed_allowed": False,
                "approval_allowed": False,
                "write_allowed": False,
            },
            {
                "state": "deferred",
                "entry_condition": "roi_better_source_or_unresolved_later",
                "allowed_transition": ["closed_no_decision"],
                "forbidden_transition": list(FORBIDDEN_STATES),
                "decision_committed_allowed": False,
                "approval_allowed": False,
                "write_allowed": False,
            },
            {
                "state": "closed_no_decision",
                "entry_condition": "dryrun_complete_no_commit",
                "allowed_transition": [],
                "forbidden_transition": list(FORBIDDEN_STATES),
                "decision_committed_allowed": False,
                "approval_allowed": False,
                "write_allowed": False,
            },
        ],
        "forbidden_states": sorted(FORBIDDEN_STATES),
    }

    trace_rows: List[Dict[str, Any]] = []
    for item in runtime_items:
        qtype = item["queue_type"]
        final = _final_status(qtype)
        steps = ["queued", "in_review_dryrun", "dryrun_evaluated", final]
        trace_rows.append(
            {
                "runtime_queue_item_id": item["runtime_queue_item_id"],
                "queue_type": qtype,
                "transition_steps": steps,
                "final_runtime_status": final,
                "decision_status": "not_committed",
                "approval_status": "not_approved",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
        item["runtime_status"] = final

    dequeue_rows: List[Dict[str, Any]] = []
    for item in sorted_items:
        qtype = item["queue_type"]
        handler = HANDLER_BY_QUEUE.get(qtype, "hold_for_review_dryrun_handler")
        dequeue_rows.append(
            {
                "runtime_queue_item_id": item["runtime_queue_item_id"],
                "queue_type": qtype,
                "priority": item["priority"],
                "dryrun_handler": handler,
                "dryrun_result": DRYRUN_RESULT_BY_QUEUE.get(qtype, "dryrun_complete_no_commit"),
                "planned_next_action": item.get("planned_next_action"),
                "blocked_actions": item.get("blocked_actions") or [],
                "final_status": item.get("runtime_status"),
                "decision_committed": False,
                "approval_status": "not_approved",
            }
        )

    handler_matrix = {
        "schema_version": "ocr_review_queue_runtime_handler_dryrun_matrix_v0",
        "handlers": [
            {
                "handler_id": "ttl_review_dryrun_handler",
                "queue_type": "ttl_review_queue",
                "dryrun_input_required": ["semantic_type_candidate", "raw_ocr_text"],
                "dryrun_output_allowed": ["ttl_review_required", "ttl_not_satisfied"],
                "dryrun_output_forbidden": ["ttl_committed", "fact_write"],
                "decision_commit_allowed": False,
                "approval_allowed": False,
                "fact_write_allowed": False,
                "world_model_attach_allowed": False,
                "scene_delta_candidate_allowed": False,
            },
            {
                "handler_id": "source_validation_dryrun_handler",
                "queue_type": "source_validation_queue",
                "dryrun_input_required": ["entity_type_candidate"],
                "dryrun_output_allowed": ["validation_required", "validation_not_satisfied"],
                "dryrun_output_forbidden": ["validation_committed"],
                "decision_commit_allowed": False,
                "approval_allowed": False,
                "fact_write_allowed": False,
                "world_model_attach_allowed": False,
                "scene_delta_candidate_allowed": False,
            },
            {
                "handler_id": "visual_symbol_registry_dryrun_handler",
                "queue_type": "visual_symbol_registry_queue",
                "dryrun_input_required": ["visual_route_id"],
                "dryrun_output_allowed": ["registry_lookup_required"],
                "dryrun_output_forbidden": ["registry_match_committed", "brand_fact"],
                "decision_commit_allowed": False,
                "approval_allowed": False,
                "fact_write_allowed": False,
                "world_model_attach_allowed": False,
                "scene_delta_candidate_allowed": False,
            },
            {
                "handler_id": "roi_retry_dryrun_handler",
                "queue_type": "roi_retry_queue",
                "dryrun_input_required": ["scan_observation_ref", "linebox_refs"],
                "dryrun_output_allowed": ["roi_retry_plan_required"],
                "dryrun_output_forbidden": ["roi_crop_executed", "fact_review"],
                "decision_commit_allowed": False,
                "approval_allowed": False,
                "fact_write_allowed": False,
                "world_model_attach_allowed": False,
                "scene_delta_candidate_allowed": False,
            },
            {
                "handler_id": "better_source_dryrun_handler",
                "queue_type": "better_source_queue",
                "dryrun_input_required": ["source_quality_grade"],
                "dryrun_output_allowed": ["better_source_required"],
                "dryrun_output_forbidden": ["strong_semantic", "ocr_request_for_SQ_E"],
                "decision_commit_allowed": False,
                "approval_allowed": False,
                "fact_write_allowed": False,
                "world_model_attach_allowed": False,
                "scene_delta_candidate_allowed": False,
            },
            {
                "handler_id": "unresolved_slot_later_dryrun_handler",
                "queue_type": "unresolved_slot_later_queue",
                "dryrun_input_required": ["scan_observation_ref"],
                "dryrun_output_allowed": ["unresolved_slot_later"],
                "dryrun_output_forbidden": ["real_slot_generated", "world_model_write"],
                "decision_commit_allowed": False,
                "approval_allowed": False,
                "fact_write_allowed": False,
                "world_model_attach_allowed": False,
                "scene_delta_candidate_allowed": False,
            },
            {
                "handler_id": "hold_for_review_dryrun_handler",
                "queue_type": "hold_for_review_queue",
                "dryrun_input_required": ["source_semantic_item_id"],
                "dryrun_output_allowed": ["held_pending_review"],
                "dryrun_output_forbidden": ["auto_approve"],
                "decision_commit_allowed": False,
                "approval_allowed": False,
                "fact_write_allowed": False,
                "world_model_attach_allowed": False,
                "scene_delta_candidate_allowed": False,
            },
        ],
    }

    placeholder_rows = []
    for item in runtime_items:
        qtype = item["queue_type"]
        placeholder_rows.append(
            {
                "runtime_queue_item_id": item["runtime_queue_item_id"],
                "decision_placeholder_id": f"dph_{item['runtime_queue_item_id']}",
                "decision_type_placeholder": f"{qtype}_decision_placeholder",
                "decision_status": "not_committed",
                "approval_status": "not_approved",
                "required_future_phase": PLANNED_ACTION_BY_QUEUE.get(qtype, "controlled_runtime_later"),
                "allowed_future_decision": ["review_after_ttl_gate", "review_after_validation"],
                "blocked_current_decision": ["approve", "commit", "fact_write", "world_model_attach"],
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    chain_rows = []
    for item in runtime_items:
        sid = item["source_semantic_item_id"]
        sem_entry = semantic_idx.get(sid, {})
        sem_ref = sem_entry.get("ref") if sem_entry else {}
        trace_ocr = False
        trace_pack = False
        trace_scan = False
        trace_visual = False
        trace_sq_e = False

        if sem_entry.get("type") == "gated":
            ib = sem_ref.get("interpretation_basis") or {}
            trace_ocr = bool((ib.get("ocr_request_ref") or {}).get("request_id"))
            trace_pack = bool((ib.get("evidence_pack_ref") or {}).get("evidence_id"))
        elif sem_entry.get("type") == "scan_hint":
            trace_scan = bool(sem_ref.get("scan_observation_ref"))
        elif sem_entry.get("type") == "visual_route":
            trace_visual = True
        elif sem_entry.get("type") == "sq_e_blocked":
            trace_sq_e = True

        chain_rows.append(
            {
                "runtime_queue_item_id": item["runtime_queue_item_id"],
                "source_review_queue_candidate_id": item["source_review_queue_candidate_id"],
                "source_semantic_item_id": sid,
                "traceable_to_semantic_v1": sid in semantic_idx,
                "traceable_to_evidence_pack_v1": trace_pack,
                "traceable_to_ocr_request": trace_ocr,
                "traceable_to_scan_observation": trace_scan,
                "traceable_to_visual_route": trace_visual,
                "traceable_to_sq_e_blocked": trace_sq_e,
                "source_chain": item.get("source_chain") or [],
                "source_chain_preserved": RUNTIME_STEP in (item.get("source_chain") or []),
            }
        )

    final_status_counts = Counter(t.get("final_runtime_status") for t in trace_rows)
    priority_counts = Counter(i["priority"] for i in runtime_items)

    metrics = {
        "schema_version": "ocr_review_queue_runtime_metrics_candidate_report_v0",
        "input_queue_candidate_count": len(candidates),
        "runtime_queue_item_count": len(runtime_items),
        "queue_type_distribution": dict(qtype_counts),
        "priority_distribution": dict(priority_counts),
        "dequeued_item_count": len(dequeue_rows),
        "held_count": final_status_counts.get("held", 0),
        "deferred_count": final_status_counts.get("deferred", 0),
        "closed_no_decision_count": final_status_counts.get("closed_no_decision", 0),
        "approval_granted_count": 0,
        "decision_committed_count": 0,
        "fact_write_allowed_count": 0,
        "world_model_attach_allowed_count": 0,
        "scene_delta_candidate_allowed_count": 0,
        "no_write_boundary_pass_rate": 1.0,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    item_schema = {
        "schema_version": "ocr_review_queue_runtime_item_schema_v1",
        "description": "Runtime queue item for OCR review queue dry-run v1",
        "template": {
            "runtime_queue_item_id": "rq_<hash>",
            "schema_version": "ocr_review_queue_runtime_item_v1",
            "source_review_queue_candidate_id": None,
            "source_semantic_item_id": None,
            "queue_type": "ttl_review_queue | source_validation_queue | visual_symbol_registry_queue | roi_retry_queue | better_source_queue | unresolved_slot_later_queue | hold_for_review_queue",
            "priority": "P0 | P1 | P2 | P3",
            "runtime_status": "queued | in_review_dryrun | dryrun_evaluated | held | deferred | rejected_from_runtime | closed_no_decision",
            "required_gates": [],
            "blocked_actions": [],
            "planned_next_action": None,
            "decision_status": "not_committed",
            "approval_status": "not_approved",
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": [],
        },
        "defaults": {
            "decision_status": "not_committed",
            "approval_status": "not_approved",
            "write_allowed": False,
            "fact_status": "not_fact",
        },
    }

    boundary = {
        "schema_version": "ocr_review_queue_runtime_boundary_report_v0",
        "runtime_queue_dryrun_only": True,
        "review_decision_committed": False,
        "approval_granted_count": 0,
        "auto_approve_invoked": False,
        "fact_review_generated": False,
        "world_model_attach_allowed": False,
        "scene_delta_candidate_allowed": False,
        "world_model_write_allowed": False,
        "navigation_decision_allowed": False,
    }

    benchmark_link = {
        "schema_version": "ocr_review_queue_runtime_benchmark_link_report_v0",
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "current_phase_collects_t2": False,
        "ground_truth_available": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": "ocr_review_queue_runtime_system_health_link_report_v0",
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    no_write = {
        "schema_version": "ocr_review_queue_runtime_no_write_boundary_report_v0",
        "boundary_ok": True,
        "violations": [],
        "runtime_dryrun_only": True,
        "review_decision_committed": False,
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
        "schema_version": "ocr_review_queue_runtime_simulation_context_report_v0",
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": "ocr_review_queue_runtime_non_claims_report_v0",
        "no_ocr_execution": True,
        "no_llm_vlm": True,
        "no_review_decision_commit": True,
        "no_candidate_approval": True,
        "no_fact_review": True,
        "no_real_ttl_judgment": True,
        "no_source_validation_execution": True,
        "no_visual_symbol_registry_lookup": True,
        "no_roi_retry_execution": True,
        "no_real_unresolved_slot": True,
        "no_world_model_attach": True,
        "no_world_model_write": True,
        "no_scene_delta": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": "ocr_review_queue_runtime_open_followups_v0",
        "items": [
            "TTL Gate v1",
            "Source Validation DryRun",
            "VisualSymbolRegistry DryRun",
            "ROI Retry Proposal Runtime",
            "Better Source Request Runtime",
            "Unresolved Slot dry-run from scan observation",
            "Review Queue persistence / storage",
            "Review Queue API contract",
            "SystemHealth provider runtime dry-run",
            "Controlled runtime integration",
        ],
    }

    audit = {
        "schema_version": "ocr_review_queue_runtime_audit_report_v0",
        "ocr_review_queue_runtime_dryrun_v1_executed": True,
        "runtime_dryrun_only": True,
        "queue_runtime_enabled": True,
        "enqueue_simulated": True,
        "priority_sort_simulated": True,
        "state_transition_simulated": True,
        "dequeue_simulated": True,
        "review_decision_committed": False,
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

    accepted = sum(1 for r in intake_rows if r.get("accepted_into_runtime_queue"))
    if accepted != len(candidates) and len(candidates) > 0:
        errs.append(f"intake_mismatch:accepted={accepted},expected={len(candidates)}")

    summary = {
        "schema_version": "ocr_review_queue_runtime_dryrun_v1_summary_v0",
        "phase": PHASE_ID,
        "runtime_scope": "review_queue_runtime_dryrun_only",
        "based_on_review_policy_v1": policy.is_dir(),
        "queue_runtime_enabled": True,
        "queue_candidate_count": len(candidates),
        "runtime_queue_item_count": len(runtime_items),
        "enqueue_simulated": True,
        "dequeue_simulated": True,
        "priority_sort_simulated": True,
        "state_transition_simulated": True,
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
        "accepted_into_runtime_queue_count": accepted,
        "phase_verdict_hint": "GO" if not errs and accepted == len(candidates) else "CONDITIONAL_GO",
    }
    if errs:
        summary["errors"] = errs

    return {
        "summary": summary,
        "item_schema": item_schema,
        "intake": {
            "schema_version": "ocr_review_queue_runtime_intake_report_v0",
            "input_queue_candidate_count": len(candidates),
            "accepted_into_runtime_queue_count": accepted,
            "rejected_from_runtime_queue_count": len(candidates) - accepted,
            "missing_required_field_count": sum(1 for r in intake_rows if not r.get("accepted_into_runtime_queue")),
            "queue_type_distribution": dict(qtype_counts),
            "intake_status": "complete" if accepted == len(candidates) else "partial",
            "duplicate_group_count": len(duplicate_groups),
            "rows": intake_rows,
        },
        "classification": classification,
        "priority_policy": priority_policy,
        "priority_sort": {
            "schema_version": "ocr_review_queue_runtime_priority_sort_report_v0",
            "row_count": len(sort_rows),
            "rows": sort_rows,
        },
        "state_plan": state_plan,
        "state_trace": {
            "schema_version": "ocr_review_queue_runtime_state_transition_trace_v0",
            "row_count": len(trace_rows),
            "rows": trace_rows,
        },
        "dequeue": {
            "schema_version": "ocr_review_queue_runtime_dequeue_dryrun_report_v0",
            "dequeue_simulated": True,
            "dequeued_item_count": len(dequeue_rows),
            "remaining_item_count": 0,
            "dequeue_order": [r["runtime_queue_item_id"] for r in dequeue_rows],
            "dequeue_policy": "priority_P0_P1_P2_P3_then_original_order",
            "decision_committed": False,
            "approval_granted": False,
            "items": dequeue_rows,
        },
        "handler_matrix": handler_matrix,
        "placeholders": {
            "schema_version": "ocr_review_queue_runtime_decision_placeholder_report_v0",
            "placeholder_count": len(placeholder_rows),
            "all_not_committed": all(p.get("decision_status") == "not_committed" for p in placeholder_rows),
            "rows": placeholder_rows,
        },
        "boundary": boundary,
        "source_chain": {
            "schema_version": "ocr_review_queue_runtime_source_chain_report_v0",
            "row_count": len(chain_rows),
            "all_traceable_to_semantic_v1": all(r.get("traceable_to_semantic_v1") for r in chain_rows),
            "rows": chain_rows,
        },
        "metrics": metrics,
        "benchmark_link": benchmark_link,
        "health_link": health_link,
        "no_write": no_write,
        "sim_report": sim_report,
        "non_claims": non_claims,
        "followups": followups,
        "audit": audit,
        "runtime_items": runtime_items,
        "errs": errs,
    }
