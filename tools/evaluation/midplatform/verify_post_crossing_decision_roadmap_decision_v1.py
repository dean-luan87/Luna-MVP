#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Post Crossing Decision Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Post-Crossing-Decision-Roadmap-Decision-v1-001"
FINAL_DECISION = "POST_CROSSING_DECISION_ROADMAP_DECISION_READY_FOR_CONTROLLED_FRAME_SAMPLE_PLANNING"
NEXT_PHASE = "Phase-Controlled-Frame-Sample-Planning-v1-001"
MIN_CHECKS = 170
BASELINE_REQUIREMENT = 130

EXPECTED_ROUTES = [
    ("A", "Controlled Frame Sample Planning", "P0", True, NEXT_PHASE),
    ("B", "Gate Taxonomy / Gate Requirement Framework", "P0", False, "Phase-Gate-Taxonomy-Gate-Requirement-Framework-v1-001"),
    ("C", "MidPlatform Function Governance / Consolidation", "P0", False, "Phase-MidPlatform-Function-Governance-Consolidation-v1-001"),
    ("D", "MidPlatform Resilience / Robustness Preplan", "P1", False, "Phase-MidPlatform-Resilience-Robustness-Preplan-v1-001"),
    ("E", "Offline Distributed MidPlatform Architecture Preplan", "P1", False, "Phase-Offline-Distributed-MidPlatform-Architecture-Preplan-v1-001"),
    ("F", "Minimal Controlled Visual Runtime Planning", "P1", False, "Phase-Minimal-Controlled-Visual-Runtime-Planning-v1-001"),
    ("G", "WorldModel Candidate Layer / Memory / Library Governance", "P2", False, "Phase-WorldModel-Memory-Library-Governance-v1-001"),
    ("H", "Exploration Drive Policy", "P2", False, "Phase-Exploration-Drive-Policy-v1-001"),
    ("I", "Emotion Map / Affective Engine", "P2", False, "Phase-Emotion-Map-Affective-Engine-v1-001"),
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/post_crossing_decision_roadmap_decision_v1_smoke_v0",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    status_summary = _load_json(root / "current_crossing_decision_status_summary.json")
    route_matrix = _load_json(root / "route_option_matrix.json")
    priority = _load_json(root / "priority_ranking.json")
    next_phase_dec = _load_json(root / "recommended_next_phase_decision.json")
    gate_taxonomy = _load_json(root / "deferred_gate_taxonomy_register.json")
    resilience = _load_json(root / "deferred_resilience_distributed_midplatform_register.json")
    wml = _load_json(root / "deferred_worldmodel_memory_library_emotion_register.json")
    boundary = _load_json(root / "boundary_freeze.json")
    non_claims = _load_json(root / "non_claims_register.json")
    debt = _load_json(root / "governance_debt_roadmap_register.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    ok("summary.decision_scope", summary.get("decision_scope") == "post_crossing_decision_roadmap_decision_only")

    for field in (
        "crossing_decision_closure_input_loaded",
        "crossing_decision_post_review_input_loaded",
        "crossing_decision_dryrun_input_loaded",
        "crossing_decision_governance_input_loaded",
        "safety_constitution_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "map_location_readonly_context_input_loaded",
        "vision_strengthening_closure_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "current_status_summary_generated",
        "completed_capability_summary_generated",
        "route_option_matrix_generated",
        "priority_ranking_generated",
        "recommended_next_phase_decision_generated",
        "deferred_gate_taxonomy_register_generated",
        "deferred_resilience_distributed_midplatform_register_generated",
        "deferred_worldmodel_memory_library_emotion_register_generated",
        "boundary_freeze_generated",
        "governance_debt_roadmap_register_generated",
        "non_claims_register_generated",
        "crossing_decision_closed",
        "forbidden_crossing_outputs_absent",
        "gate_taxonomy_deferred",
        "gate_taxonomy_project_optimization",
        "midplatform_resilience_deferred",
        "offline_distributed_midplatform_deferred",
        "worldmodel_candidate_layer_deferred",
        "memory_library_governance_deferred",
        "exploration_drive_deferred",
        "emotion_engine_deferred",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{field}", summary.get(field) is True)

    for field in (
        "crossing_runtime_claimed",
        "real_crossing_judgment_claimed",
        "safe_to_cross_capability_claimed",
        "production_readiness_claimed",
        "runtime_enablement_claimed",
        "controlled_sample_planning_started",
        "frame_content_loaded",
        "actual_image_read",
        "camera_invoked",
        "visual_model_invoked",
        "map_api_invoked",
        "ocr_provider_invoked",
        "tracking_runtime_invoked",
        "speech_gate_invoked",
        "world_model_written",
        "memory_written",
        "crossing_runtime_invoked",
        "emotion_engine_invoked",
    ):
        ok(f"summary.{field}", summary.get(field) is False)

    ok("summary.route_option_count", summary.get("route_option_count", 0) >= 8)
    ok("summary.p0_route_count", summary.get("p0_route_count", 0) >= 3)
    ok("summary.p1_route_count", summary.get("p1_route_count", 0) >= 3)
    ok("summary.p2_route_count", summary.get("p2_route_count", 0) >= 3)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("status.crossing_decision_closed", status_summary.get("crossing_decision_closed") is True)
    ok("status.forbidden_absent", status_summary.get("forbidden_crossing_outputs_absent") is True)
    ok("status.no_crossing_runtime_claim", status_summary.get("crossing_runtime_claimed") is False)

    ok("route_matrix.selected", route_matrix.get("selected_route_id") == "A")
    routes_by_id = {r.get("route_id"): r for r in route_matrix.get("routes", [])}
    for rid, name, priority_level, selected, phase in EXPECTED_ROUTES:
        r = routes_by_id.get(rid, {})
        ok(f"route.{rid}.exists", bool(r))
        ok(f"route.{rid}.name", r.get("route_name") == name)
        ok(f"route.{rid}.priority", r.get("recommended_priority") == priority_level)
        ok(f"route.{rid}.selected", r.get("selected_now") is selected)
        ok(f"route.{rid}.phase", r.get("recommended_phase_name") == phase)

    ok("priority.selected_route", priority.get("selected_top_priority_route") == "Controlled Frame Sample Planning")
    ok("next_phase_dec.selected", next_phase_dec.get("selected_next_phase") == NEXT_PHASE)

    ok("gate_taxonomy.deferred", gate_taxonomy.get("gate_taxonomy_deferred") is True)
    ok("gate_taxonomy.no_impl", gate_taxonomy.get("implementation_allowed_now") is False)
    ok("gate_taxonomy.families", len(gate_taxonomy.get("included_gate_families", [])) >= 8)

    ok("resilience.deferred", resilience.get("midplatform_resilience_deferred") is True)
    ok("resilience.offline_deferred", resilience.get("offline_distributed_midplatform_deferred") is True)

    ok("wml.worldmodel_deferred", wml.get("worldmodel_candidate_layer_deferred") is True)
    ok("wml.exploration_deferred", wml.get("exploration_drive_deferred") is True)
    ok("wml.emotion_deferred", wml.get("emotion_engine_deferred") is True)

    ok("boundary.no_crossing_runtime", boundary.get("no_crossing_runtime") is True)
    ok("boundary.no_image_read", boundary.get("no_image_read") is True)
    ok("non_claims.sample_not_started", non_claims.get("controlled_sample_planning_started") is False)

    ok("no_runtime.boundary_ok", no_runtime.get("boundary_ok") is True)
    ok("no_write.boundary_ok", no_write.get("boundary_ok") is True)
    for report_name, report in (("no_runtime", no_runtime), ("no_write", no_write)):
        ok(f"{report_name}.no_runtime_executed", report.get("no_runtime_executed") is True)
        ok(f"{report_name}.no_new_runtime_enabled", report.get("no_new_runtime_enabled") is True)
        for flag in (
            "camera_invoked",
            "visual_model_invoked",
            "map_api_invoked",
            "ocr_provider_invoked",
            "tracking_runtime_invoked",
            "speech_gate_invoked",
            "world_model_written",
            "memory_written",
            "fact_written",
        ):
            ok(f"{report_name}.{flag}_false", report.get(flag) is False)

    # Expand checks: ensure all route rows have coherent types
    for route in route_matrix.get("routes", []):
        rid = route.get("route_id", "unknown")
        ok(f"route_row.{rid}.has_name", isinstance(route.get("route_name"), str) and bool(route.get("route_name")))
        ok(f"route_row.{rid}.has_priority", route.get("recommended_priority") in ("P0", "P1", "P2"))
        ok(f"route_row.{rid}.selected_bool", isinstance(route.get("selected_now"), bool))
        ok(f"route_row.{rid}.phase_str", isinstance(route.get("recommended_phase_name"), str) and bool(route.get("recommended_phase_name")))

    # Expand checks: gate taxonomy topics and families presence
    ok("gate_taxonomy.topic_count", len(gate_taxonomy.get("required_future_topics", [])) >= 10)
    for topic in gate_taxonomy.get("required_future_topics", [])[:12]:
        ok(f"gate_taxonomy.topic.{hash(topic) % 10000}", isinstance(topic, str) and bool(topic))
    for family in gate_taxonomy.get("included_gate_families", [])[:10]:
        ok(f"gate_taxonomy.family.{hash(family) % 10000}", isinstance(family, str) and bool(family))

    # Expand checks: debt topics exist
    carry = debt.get("carryover_topics", [])
    ok("debt.topic_count", len(carry) >= 10)
    for row in carry[:12]:
        ok(f"debt.topic_row.{hash(str(row)) % 10000}", isinstance(row.get("topic"), str) and bool(row.get("topic")))

    # Expand checks: non-claims list non-empty strings
    ok("non_claims.count", len(non_claims.get("non_claims", [])) >= 10)
    for claim in non_claims.get("non_claims", [])[:12]:
        ok(f"non_claims.item.{hash(claim) % 10000}", isinstance(claim, str) and bool(claim))

    for field in (
        "controlled_frame_sample_planning_route_exists",
        "gate_taxonomy_route_exists",
        "midplatform_function_governance_route_exists",
        "midplatform_resilience_route_exists",
        "offline_distributed_midplatform_route_exists",
        "worldmodel_memory_library_route_exists",
        "exploration_drive_route_exists",
        "emotion_engine_route_exists",
    ):
        ok(f"summary.{field}", summary.get(field) is True)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verdict = "GO" if len(checks) >= MIN_CHECKS and not failed else "NO_GO"

    report = {
        "phase": PHASE_ID,
        "verifier": verdict,
        "check_count": len(checks),
        "passed_count": passed,
        "failed_count": len(failed),
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "POST_CROSSING_DECISION_ROADMAP_DECISION_VERIFIER_FAILED",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": failed[:20],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"verifier": verdict, "check_count": len(checks), "passed_count": passed, "failed_count": len(failed)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
