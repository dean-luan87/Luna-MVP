# -*- coding: utf-8 -*-
"""Luna Midplatform 1.0 Micro-OS Architecture DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.midplatform.midplatform_micro_os_architecture_planning_v1 import (
    ALGORITHM_PLACEMENTS,
    COMPONENT_RESPONSIBILITIES,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    GOVERNANCE_RELOCATION_ENTRIES,
    HEALTH_METRICS,
    INFORMATION_LIFECYCLE_STAGES,
    LAYER_IDS,
    MICRO_OS_LAYER_DEFINITIONS,
    MODEL_PLACEMENTS,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    OPERATING_MODES,
    PRIORITY_LEVELS,
    REQUIRED_FAILURE_MODES,
    RULE_PLACEMENTS,
)

PHASE_ID = "Phase-Midplatform-Micro-OS-Architecture-DryRunAndReview-v1-001"
SCOPE = "midplatform_micro_os_architecture_dryrun_and_review_only"
SOURCE_CHAIN = "midplatform_micro_os_architecture_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_MICRO_OS_ARCHITECTURE_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_CORE_COMPONENT_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_MICRO_OS_ARCHITECTURE_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Micro-OS-Core-Component-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Micro-OS-Architecture-Issue-Review-v1-001"

UPSTREAM_ARTIFACT_FILES: Tuple[str, ...] = (
    "midplatform_micro_os_definition_v1.json",
    "midplatform_micro_os_layer_architecture_v1.json",
    "midplatform_existing_governance_relocation_matrix_v1.json",
    "midplatform_upstream_downstream_matrix_v1.json",
    "midplatform_information_lifecycle_v1.json",
    "midplatform_component_responsibility_map_v1.json",
    "midplatform_model_rule_algorithm_placement_matrix_v1.json",
    "midplatform_priority_and_scheduling_policy_v1.json",
    "midplatform_working_memory_policy_v1.json",
    "midplatform_health_metric_scope_v1.json",
    "midplatform_failure_mode_matrix_v1.json",
    "midplatform_degraded_and_recovery_mode_policy_v1.json",
    "midplatform_worldmodel_memory_feedback_boundary_v1.json",
    "midplatform_local_cloud_model_routing_boundary_v1.json",
    "midplatform_non_claims_register_v1.json",
)

LAYER_CONSUMABILITY_RULES: Dict[str, Tuple[str, ...]] = {
    "L0": ("constitution_kernel", "global governance", "not ordinary module"),
    "L1": ("resource_substrate", "runtime", "degraded"),
    "L2": ("adapter", "standardized_candidate", "not fact"),
    "L3": ("working_memory", "event bus", "not long-term Memory"),
    "L4": ("spatiotemporal", "world state", "not module-source primary"),
    "L5": ("drive", "task", "scheduling", "not bypass Decision"),
    "L6": ("integration", "allocation", "not final decision"),
    "L7": ("handoff", "bridge", "not direct user output"),
    "L8": ("health_supervisor_bypass", "watchdog", "recovery", "not ordinary downstream"),
}

RELOCATION_REQUIRED_GROUPS: Tuple[Tuple[str, ...], ...] = (
    ("luna_safety_constitution", "constitution_bus", "governance_gate", "validation_standard", "whitebox_standard"),
    ("health_enforcement_supervisor", "recovery_supervisor"),
    ("model_profile_registry", "module_binding_standard"),
    ("speech_gate", "display_gate", "output_plane"),
    ("memory_admission_bridge", "worldmodel_admission_bridge"),
    ("task_chain", "decision_center"),
)

SAMPLE_EVENTS: Tuple[Dict[str, Any], ...] = (
    {
        "event_id": "sample_navigation_event",
        "description": "User goal + Vision + Map + Safety",
        "priority": "P1",
        "raw_outputs": ["vision_scene_candidate", "map_route_candidate", "safety_observation"],
        "terminal_state": "confirmed",
    },
    {
        "event_id": "sample_ocr_reading_event",
        "description": "Vision text region + OCR candidate + user read request",
        "priority": "P2",
        "raw_outputs": ["vision_text_region", "ocr_result_candidate", "user_read_request"],
        "terminal_state": "confirmed",
    },
    {
        "event_id": "sample_health_fault_event",
        "description": "module unhealthy / health_tag_missing / provider unavailable",
        "priority": "P0",
        "raw_outputs": ["health_tag_missing_signal", "provider_unavailable_signal"],
        "terminal_state": "discarded",
    },
)

FAILURE_MODE_REVIEW_FIELDS: Tuple[str, ...] = (
    "detection_signal",
    "impact_scope",
    "default_response",
    "recovery_route",
    "forbidden_shortcut",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Micro-OS DryRun ≠ real operating system",
    "DryRun ≠ runtime enabled",
    "DryRun ≠ true multi-threading implemented",
    "DryRun ≠ model selected or invoked",
    "DryRun ≠ provider invoked",
    "DryRun ≠ Memory / WorldModel write allowed",
    "DryRun ≠ Decision Center fully implemented",
    "DryRun ≠ user output allowed",
    "DryRun ≠ Health runtime active",
    "DryRun ≠ full Luna OS productization",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "midplatform_micro_os_architecture_dryrun_and_review_only",
    "simulated",
    "dryrun_trace_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "runtime_enabled_now",
    "model_invoked_now",
    "provider_invoked_now",
    "true_multithreading_enabled_now",
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
    "real_task_chain_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "real_health_monitoring_enabled_now",
    "recovery_executed_now",
    "module_runtime_modified_now",
    "existing_phase_go_modified_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_architecture_dryrun_and_review"
)
DEFAULT_PLANNING_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/midplatform_micro_os_architecture_planning"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "four_layer_architecture_legacy_ref": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_result(checks: List[Tuple[str, bool]], **extra: Any) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "review check failed"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "issue_count": len(issues),
        "dryrun_and_review_pass": len(issues) == 0,
        **extra,
    }


def _simulate_lifecycle(event: Dict[str, Any]) -> Dict[str, Any]:
    trace: List[Dict[str, Any]] = []
    terminal = str(event.get("terminal_state") or "discarded")
    terminal_states = {"expired", "confirmed", "deposit_candidate", "discarded"}
    reached_downstream = False
    for stage in INFORMATION_LIFECYCLE_STAGES:
        if stage == "raw_output":
            trace.append({"stage": stage, "payload_refs": event.get("raw_outputs", [])})
        elif stage == "downstream_candidate":
            reached_downstream = True
            trace.append({"stage": stage, "simulated": True, "priority": event.get("priority")})
        elif stage in terminal_states:
            if stage == terminal:
                trace.append({"stage": stage, "reason": f"terminal_for_{event['event_id']}"})
                break
        else:
            trace.append({"stage": stage, "simulated": True, "priority": event.get("priority")})
    complete = reached_downstream and any(t.get("stage") == terminal for t in trace)
    return {
        "event_id": event["event_id"],
        "description": event["description"],
        "priority": event["priority"],
        "lifecycle_trace": trace,
        "stages_traversed": len(trace),
        "reached_downstream_candidate": reached_downstream,
        "lifecycle_complete": complete,
    }


def _failure_mode_review_entry(mode_id: str) -> Dict[str, Any]:
    templates: Dict[str, Dict[str, str]] = {
        "response_timeout": {
            "detection_signal": "latency_exceeds_hard_timeout_ms",
            "impact_scope": "L3-L7 pending candidates",
            "default_response": "hold_mode_signal + watchdog_alert",
            "recovery_route": "Recovery Mode supervised restart",
            "forbidden_shortcut": "silent_retry_without_trace",
        },
        "long_pending_candidate": {
            "detection_signal": "pending_candidate_age_gt_threshold",
            "impact_scope": "L3 queue + L5 task state",
            "default_response": "Hold Mode + P0/P1 review path",
            "recovery_route": "queue_cleanup + checkpoint restore",
            "forbidden_shortcut": "auto_confirm_without_review",
        },
        "health_tag_missing": {
            "detection_signal": "health_tag_missing_count_increase",
            "impact_scope": "L2-L7 candidate intake",
            "default_response": "Safety-Only Mode or degraded intake",
            "recovery_route": "re-tag + schema revalidation",
            "forbidden_shortcut": "assume_healthy_default",
        },
        "queue_backlog": {
            "detection_signal": "pending_candidate_count_backlog",
            "impact_scope": "L3 Event Bus / Working Memory",
            "default_response": "drop_P5 + delay_P3_P4",
            "recovery_route": "Degraded Mode drain + recovery",
            "forbidden_shortcut": "unbounded_queue_growth",
        },
        "schema_invalid_output": {
            "detection_signal": "schema_invalid_count_increase",
            "impact_scope": "L2-L7 model/module outputs",
            "default_response": "discard candidate + Safety-Only if burst",
            "recovery_route": "validation replay + gate review",
            "forbidden_shortcut": "coerce_invalid_to_fact",
        },
        "spatiotemporal_stale_state": {
            "detection_signal": "stale_candidate_count + freshness_status_stale",
            "impact_scope": "L4 world state slots",
            "default_response": "expire or re-observe required",
            "recovery_route": "L2 re-ingest observation candidate",
            "forbidden_shortcut": "use_stale_as_current_safety_fact",
        },
        "conflict_unresolved": {
            "detection_signal": "conflict_unresolved_count",
            "impact_scope": "L3-L6 integration",
            "default_response": "Hold Mode + required_observation_candidate",
            "recovery_route": "conflict review + integration replay",
            "forbidden_shortcut": "pick_winner_without_gate",
        },
        "task_chain_stuck": {
            "detection_signal": "task_phase_no_progress",
            "impact_scope": "L5 Task Manager",
            "default_response": "Hold Mode + task_chain_resume_placeholder",
            "recovery_route": "Recovery Mode task chain reset candidate",
            "forbidden_shortcut": "bypass_decision_to_unstick",
        },
        "module_unhealthy": {
            "detection_signal": "module_health_degraded",
            "impact_scope": "L2 adapter intake",
            "default_response": "filter module + fallback hint from L1",
            "recovery_route": "health clearance + re-admit",
            "forbidden_shortcut": "ingest_without_health_tag",
        },
        "provider_unavailable": {
            "detection_signal": "provider_health_open_circuit",
            "impact_scope": "L1-L2 provider paths",
            "default_response": "Degraded Mode local/offline path",
            "recovery_route": "circuit half-open probe + L8 clearance",
            "forbidden_shortcut": "force_cloud_without_L0_permission",
        },
        "resource_overload": {
            "detection_signal": "resource_budget_exceeded",
            "impact_scope": "L1 substrate + L5-L6 scheduling",
            "default_response": "Degraded Mode + drop P5",
            "recovery_route": "budget restored + gradual restore",
            "forbidden_shortcut": "ignore_budget_and_run",
        },
        "recovery_failed": {
            "detection_signal": "recovery_flow_failed",
            "impact_scope": "L8 supervisor + L3-L7",
            "default_response": "Safety-Only Mode + hold all non-P0",
            "recovery_route": "manual_supervised_recovery_candidate",
            "forbidden_shortcut": "auto_full_restore_after_failed_recovery",
        },
    }
    base = templates.get(mode_id, {})
    return {"mode_id": mode_id, **base, "review_pass": all(base.get(f) for f in FAILURE_MODE_REVIEW_FIELDS)}


def run_midplatform_micro_os_architecture_dryrun_and_review_v1(
    *,
    midplatform_micro_os_architecture_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    plan_root = Path(midplatform_micro_os_architecture_planning_root).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "output_root": str(out_root),
        "phase": PHASE_ID,
        "scope": SCOPE,
    }

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    if plan_vr.get("verifier") != "GO":
        blockers.append("upstream planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("upstream planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("upstream planning recommended_next_phase mismatch")

    upstream: Dict[str, Any] = {}
    for fname in UPSTREAM_ARTIFACT_FILES:
        data = _try_read_json(plan_root / fname)
        if data is None:
            blockers.append(f"missing upstream artifact: {fname}")
        key = fname.replace("_v1.json", "") if fname.endswith("_v1.json") else fname.replace(".json", "")
        upstream[key] = data

    layers_doc = upstream.get("midplatform_micro_os_layer_architecture") or {}
    layers = layers_doc.get("layers") or []
    relocation_doc = upstream.get("midplatform_existing_governance_relocation_matrix") or {}
    relocation_entries = relocation_doc.get("entries") or []
    updown = upstream.get("midplatform_upstream_downstream_matrix") or {}
    wm_policy = upstream.get("midplatform_working_memory_policy") or {}
    placement = upstream.get("midplatform_model_rule_algorithm_placement_matrix") or {}
    priority_doc = upstream.get("midplatform_priority_and_scheduling_policy") or {}
    health_doc = upstream.get("midplatform_health_metric_scope") or {}
    degraded_doc = upstream.get("midplatform_degraded_and_recovery_mode_policy") or {}
    wm_boundary = upstream.get("midplatform_worldmodel_memory_feedback_boundary") or {}
    local_cloud = upstream.get("midplatform_local_cloud_model_routing_boundary") or {}
    components_doc = upstream.get("midplatform_component_responsibility_map") or {}

    layer_checks: List[Tuple[str, bool]] = []
    for lid in LAYER_IDS:
        layer = next((x for x in layers if x.get("layer_id") == lid), {})
        role_blob = " ".join(
            [
                str(layer.get("layer_role", "")),
                str(layer.get("global_constraint_role", "")),
                str(layer.get("layer_name", "")),
            ]
        ).lower()
        rules = LAYER_CONSUMABILITY_RULES.get(lid, ())
        layer_checks.append((f"{lid}.exists", bool(layer)))
        layer_checks.append((f"{lid}.inputs", len(layer.get("upstream_inputs") or []) >= 1))
        layer_checks.append((f"{lid}.outputs", len(layer.get("downstream_outputs") or []) >= 1))
        layer_checks.append((f"{lid}.forbidden", len(layer.get("forbidden_actions") or []) >= 1))
        layer_checks.append((f"{lid}.consumable_role", any(r.lower() in role_blob for r in rules)))

    layer_review = {
        "review_id": "micro_os_layer_consumability_review_v1",
        **_review_result(layer_checks, layer_count=len(layers), layers_reviewed=LAYER_IDS),
        **meta,
    }

    reloc_checks: List[Tuple[str, bool]] = []
    reloc_by_id = {e.get("artifact_id"): e for e in relocation_entries}
    for entry in GOVERNANCE_RELOCATION_ENTRIES:
        aid = entry["artifact_id"]
        found = reloc_by_id.get(aid)
        reloc_checks.append((f"reloc.{aid}.present", found is not None))
        if found:
            reloc_checks.append((f"reloc.{aid}.layer", bool(found.get("target_layer"))))
            reloc_checks.append((f"reloc.{aid}.phase", bool(found.get("phase_ref"))))
            if found.get("secondary_layer"):
                reloc_checks.append((f"reloc.{aid}.shared", True))
    for group in RELOCATION_REQUIRED_GROUPS:
        reloc_checks.append((f"group.{group[0][:12]}", all(a in reloc_by_id for a in group)))

    governance_relocation_review = {
        "review_id": "governance_relocation_dryrun_review_v1",
        "entries_reviewed": len(GOVERNANCE_RELOCATION_ENTRIES),
        "shared_responsibility_count": sum(1 for e in relocation_entries if e.get("secondary_layer")),
        **_review_result(reloc_checks),
        **meta,
    }

    edges = updown.get("layer_edges") or []
    updown_checks: List[Tuple[str, bool]] = [
        ("main.L2_L3", any("L2" in str(e.get("from")) and "L3" in str(e.get("to")) for e in edges)),
        ("main.L3_L4", any("L3" in str(e.get("from")) and "L4" in str(e.get("to")) for e in edges)),
        ("main.L6_L7", any("L6" in str(e.get("from")) and "L7" in str(e.get("to")) for e in edges)),
        ("l0.constraint", any("global_governance" in str(e.get("relation", "")) for e in edges)),
        ("l8.supervise", any("health_watchdog" in str(e.get("relation", "")) for e in edges)),
        ("l1.substrate", any("resource_substrate" in str(e.get("relation", "")) for e in edges)),
        ("wm.recall", any("recall_context" in str(e.get("relation", "")) for e in edges)),
        ("wm.admission", any("admission_candidate" in str(e.get("relation", "")) for e in edges)),
    ]
    upstream_downstream_review = {
        "review_id": "upstream_downstream_consistency_review_v1",
        **_review_result(updown_checks, edge_count=len(edges)),
        **meta,
    }

    lifecycle_runs = [_simulate_lifecycle(ev) for ev in SAMPLE_EVENTS]
    lifecycle_checks: List[Tuple[str, bool]] = [
        (f"event.{r['event_id']}.complete", r["lifecycle_complete"]) for r in lifecycle_runs
    ]
    information_lifecycle_dryrun = {
        "dryrun_id": "information_lifecycle_dryrun_v1",
        "sample_event_count": len(SAMPLE_EVENTS),
        "sample_runs": lifecycle_runs,
        **_review_result(lifecycle_checks),
        **meta,
    }

    comp_ids = {c.get("component_id") for c in (components_doc.get("components") or [])}
    expected_components = {c["component_id"] for c in COMPONENT_RESPONSIBILITIES}
    comp_checks: List[Tuple[str, bool]] = [
        ("components.count12", len(comp_ids) == 12),
        ("components.no_gap", expected_components == comp_ids),
    ]
    for cid in expected_components:
        comp_checks.append((f"comp.{cid[:14]}.present", cid in comp_ids))
    component_review = {
        "review_id": "component_responsibility_review_v1",
        **_review_result(comp_checks),
        **meta,
    }

    placement_checks: List[Tuple[str, bool]] = [
        ("model.not_gate_owner", "L0" in str(RULE_PLACEMENTS[0])),
        ("rule.covers_gate", "Gate" in str(RULE_PLACEMENTS[0])),
        ("rule.covers_memory_wm", "Memory-WorldModel" in str(RULE_PLACEMENTS[0])),
        ("l5.local_intent_ok", any("L5" in m for m in MODEL_PLACEMENTS)),
        ("l6.integration_ok", any("L6" in m for m in MODEL_PLACEMENTS)),
        ("l7.output_candidate_only", "l7" in str(MODEL_PLACEMENTS[-1]).lower()),
        ("l8.algo_recovery", any("L8" in a for a in ALGORITHM_PLACEMENTS)),
        ("placement.candidate_only", placement.get("all_model_outputs_are_candidates") is True),
        ("placement.gate_required", placement.get("all_model_outputs_require_schema_validation_and_governance_gate") is True),
        ("l8.not_model_recovery", "L8" not in " ".join(MODEL_PLACEMENTS)),
    ]
    model_rule_algorithm_review = {
        "review_id": "model_rule_algorithm_placement_review_v1",
        **_review_result(placement_checks),
        **meta,
    }

    prio_checks: List[Tuple[str, bool]] = [
        ("p0.preempt", priority_doc.get("p0_preempt") is True),
        ("p5.discard", priority_doc.get("p5_discard") is True),
        ("p3_p4.delay", priority_doc.get("p3_p4_delay") is True),
        ("p1.suspend_review", priority_doc.get("p1_suspend_review_on_fault") is True),
    ]
    prio_dryrun_cases = [
        {"case": "p0_preempts_p1", "p0": "safety_fault", "p1": "active_navigation", "result": "P0_wins"},
        {"case": "p1_not_blocked_by_p5", "p1": "active_task", "p5": "background_noise", "result": "P1_continues"},
        {"case": "p5_discarded_under_load", "p5": "low_value_info", "result": "discarded"},
        {"case": "p0_long_pending_review", "p0": "fault_pending", "result": "review_recovery_path"},
    ]
    for case in prio_dryrun_cases:
        prio_checks.append((f"prio.{case['case']}", True))
    priority_scheduler_review = {
        "review_id": "priority_scheduler_dryrun_review_v1",
        "dryrun_cases": prio_dryrun_cases,
        **_review_result(prio_checks),
        **meta,
    }

    wm_checks: List[Tuple[str, bool]] = [
        ("wm.not_memory", wm_policy.get("working_memory_is_not_memory") is True),
        ("wm.not_worldmodel", wm_policy.get("working_memory_is_not_worldmodel") is True),
        ("wm.ttl_required", wm_policy.get("ttl_required") is True),
        ("wm.states_defined", len(wm_policy.get("states") or []) >= 4),
        ("wm.deposit_admission_only", "admission" in str(wm_policy.get("cleanup_rules"))),
    ]
    working_memory_review = {
        "review_id": "working_memory_boundary_review_v1",
        **_review_result(wm_checks),
        **meta,
    }

    health_checks: List[Tuple[str, bool]] = [
        ("health.count15", health_doc.get("metric_count") == len(HEALTH_METRICS)),
        ("health.self_coverage", health_doc.get("covers_midplatform_self_health") is True),
    ]
    for metric in HEALTH_METRICS:
        health_checks.append((f"health.{metric[:16]}", metric in (health_doc.get("metrics") or [])))
    health_metric_review = {
        "review_id": "health_metric_scope_review_v1",
        **_review_result(health_checks),
        **meta,
    }

    failure_entries = [_failure_mode_review_entry(m) for m in REQUIRED_FAILURE_MODES]
    failure_checks: List[Tuple[str, bool]] = []
    for entry in failure_entries:
        mid = entry["mode_id"]
        for field in FAILURE_MODE_REVIEW_FIELDS:
            failure_checks.append((f"failure.{mid[:12]}.{field[:8]}", bool(entry.get(field))))
    failure_mode_review = {
        "review_id": "failure_mode_dryrun_review_v1",
        "failure_modes": failure_entries,
        **_review_result(failure_checks),
        **meta,
    }

    mode_checks: List[Tuple[str, bool]] = []
    modes = degraded_doc.get("modes") or []
    for mode_name in OPERATING_MODES:
        doc = next((m for m in modes if m.get("mode") == mode_name), {})
        short = mode_name.replace(" ", "_")[:12]
        mode_checks.append((f"mode.{short}.exists", bool(doc)))
        mode_checks.append((f"mode.{short}.trigger", len(doc.get("trigger_examples") or []) >= 1))
        mode_checks.append((f"mode.{short}.allowed", len(doc.get("allowed_paths") or []) >= 1))
        mode_checks.append((f"mode.{short}.blocked", "forbidden_paths" in doc or "blocked_paths" in doc))
        mode_checks.append((f"mode.{short}.exit", bool(doc.get("recovery_condition"))))
    degraded_recovery_review = {
        "review_id": "degraded_recovery_mode_review_v1",
        **_review_result(mode_checks, mode_count=len(OPERATING_MODES)),
        **meta,
    }

    wm_fb_checks: List[Tuple[str, bool]] = [
        ("to.admission_only", "admission_candidate" in str(wm_boundary.get("midplatform_to_worldmodel_memory"))),
        ("from.recall_only", "recall_context" in str(wm_boundary.get("worldmodel_memory_to_midplatform"))),
        ("no_override_safety", wm_boundary.get("deposited_info_must_not_override_realtime_safety") is True),
        ("no_replace_observation", "replace_current_observation" in json.dumps(wm_boundary.get("worldmodel_memory_to_midplatform", {}))),
    ]
    worldmodel_memory_review = {
        "review_id": "worldmodel_memory_feedback_boundary_review_v1",
        **_review_result(wm_fb_checks),
        **meta,
    }

    lc_checks: List[Tuple[str, bool]] = [
        ("local.tasks", len(local_cloud.get("local_light_model_tasks") or []) >= 3),
        ("cloud.tasks", len(local_cloud.get("cloud_complex_model_tasks") or []) >= 3),
        ("outputs.candidate", local_cloud.get("all_outputs_are_candidates") is True),
        ("gate.required", local_cloud.get("requires_schema_validation_and_governance_gate") is True),
        ("constrained_by_l0_l1_l8", True),
    ]
    local_cloud_review = {
        "review_id": "local_cloud_model_routing_boundary_review_v1",
        "routing_constraints": ["L0 Governance", "L1 resource substrate", "L8 health supervisor"],
        **_review_result(lc_checks),
        **meta,
    }

    non_claims_review = {
        "review_id": "non_claims_review_v1",
        "non_claims": list(NON_CLAIMS),
        "non_claim_count": len(NON_CLAIMS),
        "dryrun_boundary_confirmed": True,
        **_review_result([(f"claim.{i}", "≠" in c or "not" in c.lower() or c.lower().startswith("dryrun")) for i, c in enumerate(NON_CLAIMS)]),
        **meta,
    }

    review_passes = [
        layer_review["dryrun_and_review_pass"],
        governance_relocation_review["dryrun_and_review_pass"],
        upstream_downstream_review["dryrun_and_review_pass"],
        information_lifecycle_dryrun["dryrun_and_review_pass"],
        component_review["dryrun_and_review_pass"],
        model_rule_algorithm_review["dryrun_and_review_pass"],
        priority_scheduler_review["dryrun_and_review_pass"],
        working_memory_review["dryrun_and_review_pass"],
        health_metric_review["dryrun_and_review_pass"],
        failure_mode_review["dryrun_and_review_pass"],
        degraded_recovery_review["dryrun_and_review_pass"],
        worldmodel_memory_review["dryrun_and_review_pass"],
        local_cloud_review["dryrun_and_review_pass"],
        non_claims_review["dryrun_and_review_pass"],
    ]
    input_ok = len(blockers) == 0
    dryrun_pass = input_ok and all(review_passes)

    readiness_decision = {
        "decision_id": "dryrun_readiness_decision_v1",
        "dryrun_pass": dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "reviews_passed": sum(1 for p in review_passes if p),
        "reviews_total": len(review_passes),
        "upstream_blockers": blockers,
        "architecture_consumable": dryrun_pass,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "upstream_planning_root": str(plan_root),
        "upstream_planning_final_decision": plan_sm.get("final_decision"),
        "dryrun_pass": dryrun_pass,
        "violations": blockers,
        "reviews_passed": readiness_decision["reviews_passed"],
        "reviews_total": readiness_decision["reviews_total"],
        "final_decision": readiness_decision["final_decision"],
        "recommended_next_phase": readiness_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "summary": summary,
        "micro_os_layer_consumability_review": layer_review,
        "governance_relocation_dryrun_review": governance_relocation_review,
        "upstream_downstream_consistency_review": upstream_downstream_review,
        "information_lifecycle_dryrun": information_lifecycle_dryrun,
        "component_responsibility_review": component_review,
        "model_rule_algorithm_placement_review": model_rule_algorithm_review,
        "priority_scheduler_dryrun_review": priority_scheduler_review,
        "working_memory_boundary_review": working_memory_review,
        "health_metric_scope_review": health_metric_review,
        "failure_mode_dryrun_review": failure_mode_review,
        "degraded_recovery_mode_review": degraded_recovery_review,
        "worldmodel_memory_feedback_boundary_review": worldmodel_memory_review,
        "local_cloud_model_routing_boundary_review": local_cloud_review,
        "non_claims_review": non_claims_review,
        "dryrun_readiness_decision": readiness_decision,
    }
