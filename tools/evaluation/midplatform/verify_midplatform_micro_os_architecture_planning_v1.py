#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Midplatform 1.0 Micro-OS Architecture Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.midplatform_micro_os_architecture_planning_v1 import (
    ALGORITHM_PLACEMENTS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    COMPONENT_RESPONSIBILITIES,
    FINAL_DECISION_GO,
    GOVERNANCE_RELOCATION_ENTRIES,
    HEALTH_METRICS,
    INFORMATION_LIFECYCLE_STAGES,
    LAYER_IDS,
    MICRO_OS_LAYER_DEFINITIONS,
    MODEL_PLACEMENTS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OPERATING_MODES,
    PHASE_ID,
    PRIORITY_LEVELS,
    REQUIRED_FAILURE_MODES,
    RULE_PLACEMENTS,
    SCOPE,
)

MIN_CHECKS = 351

REQUIRED = (
    "summary.json",
    "midplatform_micro_os_architecture_planning_policy_v1.json",
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
    "midplatform_micro_os_dryrun_plan_v1.json",
    "midplatform_micro_os_architecture_planning_decision_v1.json",
)

RELOCATION_REQUIRED_IDS = (
    "luna_safety_constitution",
    "constitution_bus",
    "governance_gate",
    "validation_standard",
    "whitebox_standard",
    "health_enforcement_supervisor",
    "model_profile_registry",
    "module_binding_standard",
    "information_integration_layer",
    "decision_center",
    "speech_gate",
    "display_gate",
    "output_plane",
    "memory_admission_bridge",
    "worldmodel_admission_bridge",
    "task_chain",
    "recovery_supervisor",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=str(_REPO_ROOT / "_tmp_eval_out" / "midplatform_micro_os_architecture_planning"),
    )
    p.add_argument("--output", default="")
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for fname in REQUIRED:
        ok(f"file.{fname[:24]}", (root / fname).is_file())

    ok("phase.id", PHASE_ID.endswith("-001"))
    ok("scope", SCOPE == "midplatform_micro_os_architecture_planning_only")

    summary = _load(root / "summary.json")
    decision = _load(root / "midplatform_micro_os_architecture_planning_decision_v1.json")
    policy = _load(root / "midplatform_micro_os_architecture_planning_policy_v1.json")
    definition = _load(root / "midplatform_micro_os_definition_v1.json")
    layers_doc = _load(root / "midplatform_micro_os_layer_architecture_v1.json")
    relocation = _load(root / "midplatform_existing_governance_relocation_matrix_v1.json")
    updown = _load(root / "midplatform_upstream_downstream_matrix_v1.json")
    lifecycle = _load(root / "midplatform_information_lifecycle_v1.json")
    components = _load(root / "midplatform_component_responsibility_map_v1.json")
    placement = _load(root / "midplatform_model_rule_algorithm_placement_matrix_v1.json")
    priority = _load(root / "midplatform_priority_and_scheduling_policy_v1.json")
    wm_policy = _load(root / "midplatform_working_memory_policy_v1.json")
    health = _load(root / "midplatform_health_metric_scope_v1.json")
    failure = _load(root / "midplatform_failure_mode_matrix_v1.json")
    degraded = _load(root / "midplatform_degraded_and_recovery_mode_policy_v1.json")
    wm_boundary = _load(root / "midplatform_worldmodel_memory_feedback_boundary_v1.json")
    local_cloud = _load(root / "midplatform_local_cloud_model_routing_boundary_v1.json")
    non_claims = _load(root / "midplatform_non_claims_register_v1.json")
    dryrun = _load(root / "midplatform_micro_os_dryrun_plan_v1.json")

    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("policy.layer9", policy.get("layer_count") == 9)
    ok("policy.scope", policy.get("scope") == SCOPE)
    ok("def.micro_os", "Micro-OS" in str(definition.get("midplatform_1_0_form", "")))

    for lid in LAYER_IDS:
        ok(f"layer.{lid}.defined", any(x["layer_id"] == lid for x in MICRO_OS_LAYER_DEFINITIONS))
    ok("layers.count9", layers_doc.get("layer_count") == 9)
    ok("layers.l0_governance", layers_doc.get("l0_global_governance_constraint") is True)
    ok("layers.l8_bypass", layers_doc.get("l8_global_supervisory_bypass") is True)
    ok("layers.l1_substrate", layers_doc.get("l1_resource_substrate_for_l2_l7") is True)

    l0 = next(x for x in layers_doc.get("layers", []) if x.get("layer_id") == "L0")
    l8 = next(x for x in layers_doc.get("layers", []) if x.get("layer_id") == "L8")
    ok("l0.constitution_role", l0.get("global_constraint_role") == "constitution_kernel")
    ok("l8.supervisor_role", l8.get("global_constraint_role") == "health_supervisor_bypass")

    relocation_ids = {e.get("artifact_id") for e in relocation.get("entries", [])}
    for rid in RELOCATION_REQUIRED_IDS:
        ok(f"reloc.{rid[:16]}", rid in relocation_ids)
    ok("reloc.count", relocation.get("entry_count") == len(GOVERNANCE_RELOCATION_ENTRIES))

    ok("updown.edges", len(updown.get("layer_edges", [])) >= 8)
    ok("updown.l0_constraint", any(e.get("relation") == "global_governance_constraint" for e in updown.get("layer_edges", [])))
    ok("updown.l8_supervise", any("health_watchdog" in str(e.get("relation", "")) for e in updown.get("layer_edges", [])))

    ok("lifecycle.count", lifecycle.get("stage_count") == len(INFORMATION_LIFECYCLE_STAGES))
    for stage in INFORMATION_LIFECYCLE_STAGES:
        ok(f"lifecycle.{stage[:12]}", stage in (lifecycle.get("stages") or []))

    ok("components.count", components.get("component_count") == len(COMPONENT_RESPONSIBILITIES))
    ok("wm.not_memory", wm_policy.get("working_memory_is_not_memory") is True)
    ok("wm.not_worldmodel", wm_policy.get("working_memory_is_not_worldmodel") is True)
    ok("wm.ttl", wm_policy.get("ttl_required") is True)

    ok("placement.model", len(placement.get("model_placements") or []) == len(MODEL_PLACEMENTS))
    ok("placement.rule", len(placement.get("rule_placements") or []) == len(RULE_PLACEMENTS))
    ok("placement.algo", len(placement.get("algorithm_placements") or []) == len(ALGORITHM_PLACEMENTS))
    ok("placement.candidate_only", placement.get("all_model_outputs_are_candidates") is True)
    ok("placement.gate_required", placement.get("all_model_outputs_require_schema_validation_and_governance_gate") is True)

    ok("priority.p0", any(p.get("priority") == "P0" for p in priority.get("priorities", [])))
    ok("priority.p5", any(p.get("priority") == "P5" for p in priority.get("priorities", [])))
    ok("priority.preempt", priority.get("p0_preempt") is True)
    ok("priority.discard", priority.get("p5_discard") is True)
    ok("priority.delay", priority.get("p3_p4_delay") is True)

    ok("health.count", health.get("metric_count") == len(HEALTH_METRICS))
    for metric in HEALTH_METRICS:
        ok(f"health.{metric[:16]}", metric in (health.get("metrics") or []))

    failure_ids = {m.get("mode_id") for m in failure.get("failure_modes", [])}
    for mode in REQUIRED_FAILURE_MODES:
        ok(f"failure.{mode[:16]}", mode in failure_ids)

    ok("degraded.modes5", len(degraded.get("modes", [])) == len(OPERATING_MODES))
    for mode in OPERATING_MODES:
        ok(f"degraded.{mode[:10]}", any(m.get("mode") == mode for m in degraded.get("modes", [])))

    ok("wm_bridge.admission_only", "admission_candidate" in str(wm_boundary.get("midplatform_to_worldmodel_memory")))
    ok("wm_bridge.recall_only", "recall_context" in str(wm_boundary.get("worldmodel_memory_to_midplatform")))
    ok("wm_bridge.no_override", wm_boundary.get("deposited_info_must_not_override_realtime_safety") is True)

    ok("local_cloud.local", len(local_cloud.get("local_light_model_tasks") or []) >= 3)
    ok("local_cloud.cloud", len(local_cloud.get("cloud_complex_model_tasks") or []) >= 3)
    ok("local_cloud.candidate", local_cloud.get("all_outputs_are_candidates") is True)

    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= len(NON_CLAIMS))
    for i, claim in enumerate(NON_CLAIMS):
        ok(f"non_claims.{i}", claim in (non_claims.get("non_claims") or []))

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    for layer in layers_doc.get("layers", []):
        lid = layer.get("layer_id", "")
        ok(f"layerdoc.{lid}.name", bool(layer.get("layer_name")))
        ok(f"layerdoc.{lid}.role", bool(layer.get("layer_role")))
        ok(f"layerdoc.{lid}.inputs", len(layer.get("upstream_inputs") or []) >= 1)
        ok(f"layerdoc.{lid}.outputs", len(layer.get("downstream_outputs") or []) >= 1)
        ok(f"layerdoc.{lid}.forbidden", len(layer.get("forbidden_actions") or []) >= 1)
        ok(f"layerdoc.{lid}.artifacts", len(layer.get("placed_artifacts") or []) >= 1)

    for entry in relocation.get("entries", []):
        aid = str(entry.get("artifact_id") or "unknown")
        ok(f"relocdoc.{aid[:14]}.layer", bool(entry.get("target_layer")))
        ok(f"relocdoc.{aid[:14]}.phase", bool(entry.get("phase_ref")))

    for comp in components.get("components", []):
        cid = str(comp.get("component_id") or "unknown")
        ok(f"comp.{cid[:14]}.layer", bool(comp.get("primary_layer")))
        ok(f"comp.{cid[:14]}.role", bool(comp.get("role")))

    for prio in priority.get("priorities", []):
        p = str(prio.get("priority") or "")
        ok(f"prio.{p}.name", bool(prio.get("name")))
        ok(f"prio.{p}.policy", bool(prio.get("policy")))

    for mode_doc in degraded.get("modes", []):
        mode = str(mode_doc.get("mode") or "")
        ok(f"mode.{mode[:8]}.trigger", len(mode_doc.get("trigger_examples") or []) >= 1)
        ok(f"mode.{mode[:8]}.allowed", len(mode_doc.get("allowed_paths") or []) >= 1)
        ok(f"mode.{mode[:8]}.forbidden", "forbidden_paths" in mode_doc)
        ok(f"mode.{mode[:8]}.recovery", bool(mode_doc.get("recovery_condition")))

    for stage in ("raw_output", "standardized_candidate", "working_memory_entry", "allocation_result", "discarded"):
        ok(f"lifecycle.key.{stage[:10]}", stage in (lifecycle.get("stages") or []))

    for model_place in MODEL_PLACEMENTS:
        ok(f"modelplace.{model_place[:12]}", model_place in (placement.get("model_placements") or []))
    for rule_place in RULE_PLACEMENTS:
        ok(f"ruleplace.{rule_place[:12]}", rule_place in (placement.get("rule_placements") or []))
    for algo_place in ALGORITHM_PLACEMENTS:
        ok(f"algoplace.{algo_place[:12]}", algo_place in (placement.get("algorithm_placements") or []))

    ok("wm_bridge.to.forbidden", "direct_write" in str(wm_boundary.get("midplatform_to_worldmodel_memory")))
    ok("wm_bridge.from.forbidden", "override_realtime_safety" in str(wm_boundary.get("worldmodel_memory_to_midplatform")))
    ok("local_cloud.gate", local_cloud.get("requires_schema_validation_and_governance_gate") is True)
    ok("reloc.covers_flags", relocation.get("covers_constitution_governance_validation_whitebox") is True)
    ok("reloc.prior_go", relocation.get("prior_phase_go_conclusions_unchanged") is True)
    ok("def.not_device_os", "device-level OS" in str(definition.get("non_responsibilities")))
    ok("def.not_memory_write", "direct Memory/WorldModel writes" in str(definition.get("non_responsibilities")))
    ok("layers.bidirectional_note", "admission" in str(layers_doc.get("worldmodel_memory_bidirectional_note", "")).lower())

    for field in BOUNDARY_TRUE:
        ok(f"boundary.true.{field[:16]}", policy.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.false.{field[:16]}", policy.get(field) is False)

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    all_pass = passed == total and passed >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "min_checks": MIN_CHECKS,
        "checks_run": total,
        "checks_passed": passed,
        "all_pass": all_pass,
        "verifier": "GO" if all_pass else "HOLD",
        "checks": checks,
    }
    out_path = Path(args.output) if args.output else (root / "verify_midplatform_micro_os_architecture_planning_v1.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    verifier_report = root / "verifier_report.json"
    verifier_report.write_text(
        json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_run": total}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(str(out_path))
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
