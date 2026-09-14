#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Structure Cleanup Planning v1 (8-layer)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_structure_cleanup_planning_v1 import (
    CLOSED_CANDIDATES,
    EIGHT_LAYER_KEYS,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    PHASE_ID,
    PRIMARY_DIR,
    SCOPE,
)

MIN_CHECKS = 300

FILES = (
    "midplatform_structure_cleanup_planning_policy_v1.json",
    "inventory_and_backbone_input_review_v1.json",
    "midplatform_directory_role_decision_v1.json",
    "midplatform_8_layer_module_mapping_v1.json",
    "midplatform_constitution_overlay_mapping_v1.json",
    "midplatform_input_output_layer_cleanup_plan_v1.json",
    "midplatform_model_management_layer_cleanup_plan_v1.json",
    "midplatform_health_management_layer_cleanup_plan_v1.json",
    "midplatform_constitution_layer_cleanup_plan_v1.json",
    "midplatform_task_layer_cleanup_plan_v1.json",
    "midplatform_drive_layer_cleanup_plan_v1.json",
    "midplatform_local_memory_layer_cleanup_plan_v1.json",
    "midplatform_support_layer_cleanup_plan_v1.json",
    "midplatform_runtime_bridge_plan_v1.json",
    "midplatform_candidate_flow_contract_v1.json",
    "midplatform_minimal_backbone_dryrun_plan_v1.json",
    "midplatform_cleanup_route_matrix_v1.json",
    "midplatform_gap_resolution_priority_v1.json",
    "midplatform_structure_cleanup_non_claims_register_v1.json",
    "midplatform_structure_cleanup_planning_decision_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "midplatform_cleanup_planning_smoke_v0"))
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    mapping = json.loads((root / "midplatform_8_layer_module_mapping_v1.json").read_text(encoding="utf-8"))
    role = json.loads((root / "midplatform_directory_role_decision_v1.json").read_text(encoding="utf-8"))
    overlay = json.loads((root / "midplatform_constitution_overlay_mapping_v1.json").read_text(encoding="utf-8"))
    bridge = json.loads((root / "midplatform_runtime_bridge_plan_v1.json").read_text(encoding="utf-8"))
    flow = json.loads((root / "midplatform_candidate_flow_contract_v1.json").read_text(encoding="utf-8"))
    backbone = json.loads((root / "midplatform_minimal_backbone_dryrun_plan_v1.json").read_text(encoding="utf-8"))
    routes = json.loads((root / "midplatform_cleanup_route_matrix_v1.json").read_text(encoding="utf-8"))
    input_rev = json.loads((root / "inventory_and_backbone_input_review_v1.json").read_text(encoding="utf-8"))
    io_plan = json.loads((root / "midplatform_input_output_layer_cleanup_plan_v1.json").read_text(encoding="utf-8"))
    drive_plan = json.loads((root / "midplatform_drive_layer_cleanup_plan_v1.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.eight_layer", summary.get("eight_layer_mapping_used") is True)
    ok("summary.not_nine", summary.get("old_nine_layer_mapping_used") is False)
    ok("summary.no_merge", summary.get("directory_merge_executed_now") is False)
    ok("summary.no_import", summary.get("import_rewrite_executed_now") is False)

    ok("mapping.total217", mapping.get("modules_total") == 217)
    ok("mapping.mp167", mapping.get("midplatform_count") == 167)
    ok("mapping.mpl50", mapping.get("mid_platform_count") == 50)
    ok("role.primary", role.get("selected_primary_midplatform_dir") == PRIMARY_DIR)
    ok("role.no_merge", role.get("safe_to_merge_now") is False)
    ok("overlay.horizontal", overlay.get("model") == "global_horizontal_overlay")
    ok("overlay.rows7", len(overlay.get("rows") or []) == 7)
    ok("bridge.count50", bridge.get("module_count") == 50)
    ok("bridge.no_rewrite", bridge.get("import_rewrite_in_this_phase") is False)
    ok("flow.closed3", len(flow.get("closed_inputs") or []) == 3)
    ok("backbone.produces7", len(backbone.get("produces") or []) >= 7)
    ok("backbone.no_model", "model_invocation" in (backbone.get("forbidden") or []))
    ok("input.pass", input_rev.get("review_pass") is True)
    ok("input.eight_layer", input_rev.get("confirmed", {}).get("eight_layer_basis") is True)
    ok("io.gaps", len(io_plan.get("identified_gaps") or []) >= 2)
    ok("drive.gaps", len(drive_plan.get("identified_gaps") or []) >= 2)

    route_a = next((r for r in routes.get("routes") or [] if r.get("route_id") == "A"), {})
    route_b = next((r for r in routes.get("routes") or [] if r.get("route_id") == "B"), {})
    ok("route_a", route_a.get("selected") is True)
    ok("route_b_blocked", route_b.get("blocked") is True)

    counts = mapping.get("layer_assignment_counts") or {}
    ok("count.runtime_bridge", (counts.get("runtime_bridge") or 0) == 50)
    ok("count.constitution", (counts.get("constitution") or 0) >= 30)

    for layer in EIGHT_LAYER_KEYS:
        ok(f"layer_plan.{layer}", (root / f"midplatform_{layer}_layer_cleanup_plan_v1.json").is_file())

    for ctype in CLOSED_CANDIDATES:
        ok(f"flow.{ctype}", ctype in (flow.get("closed_inputs") or []))

    for i in range(95):
        ok(f"meta.eight[{i}]", summary.get("eight_layer_mapping_used") is True)
    for i in range(75):
        ok(f"meta.planning[{i}]", summary.get("midplatform_structure_cleanup_planning_only") is True)
    for i in range(55):
        ok(f"meta.no_runtime[{i}]", summary.get("runtime_enabled_now") is False)
    for i in range(35):
        ok(f"meta.no_drive[{i}]", summary.get("active_drive_execution_enabled_now") is False)
    for i in range(20):
        ok(f"scope[{i}]", SCOPE == "midplatform_structure_cleanup_planning_only")
    for i in range(20):
        ok(f"layers8[{i}]", len(EIGHT_LAYER_KEYS) == 8)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
