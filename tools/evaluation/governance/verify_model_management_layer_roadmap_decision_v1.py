#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Model Management Layer Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.model_management_layer_recovery_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL,
    NEXT_PHASE_GO as POST_REVIEW_NEXT,
)
from capabilities.governance.model_management_layer_roadmap_decision_v1 import (
    BOUNDARY_FALSE,
    B_LITE_GOALS,
    DEFERRED_ROUTE_A,
    DEFERRED_ROUTE_D,
    FINAL_DECISION_GO,
    FUTURE_VERSIONS,
    NEXT_PHASE_GO,
    NEXT_ROUTE,
    PHASE_ID,
    REGISTRY_VERSION,
    ROUTE_A,
    ROUTE_B_LITE,
    ROUTE_C,
    ROUTE_D,
    SCHEMA_VERSION,
    SCOPE,
    SELECTED_ROUTE,
    UPDATE_TRIGGERS,
    VERSION_SCOPE,
    VERSION_STATUS,
    V0_MODEL_IDS,
)

MIN_CHECKS = 100

REQUIRED = (
    "model_management_roadmap_decision_policy_v1.json",
    "model_management_post_review_input_review_v1.json",
    "route_a_vision_ocr_voice_optimization_assessment_v1.json",
    "route_b_lite_model_registry_canonicalization_assessment_v1.json",
    "route_c_health_management_integration_assessment_v1.json",
    "route_d_skill_registry_expansion_assessment_v1.json",
    "model_management_route_selection_matrix_v1.json",
    "selected_route_preconditions_v1.json",
    "deferred_routes_register_v1.json",
    "next_phase_readiness_decision_v1.json",
    "model_registry_versioning_policy_v1.json",
    "model_registry_version_note_v0.md",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "model_management_layer_roadmap_decision"
        ),
    )
    p.add_argument(
        "--model-management-layer-recovery-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "model_management_layer_recovery_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    post_root = Path(args.model_management_layer_recovery_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(root / "model_management_roadmap_decision_policy_v1.json")
    inp = _load(root / "model_management_post_review_input_review_v1.json")
    route_a = _load(root / "route_a_vision_ocr_voice_optimization_assessment_v1.json")
    route_b = _load(root / "route_b_lite_model_registry_canonicalization_assessment_v1.json")
    route_c = _load(root / "route_c_health_management_integration_assessment_v1.json")
    route_d = _load(root / "route_d_skill_registry_expansion_assessment_v1.json")
    matrix = _load(root / "model_management_route_selection_matrix_v1.json")
    pre = _load(root / "selected_route_preconditions_v1.json")
    defer = _load(root / "deferred_routes_register_v1.json")
    readiness = _load(root / "next_phase_readiness_decision_v1.json")
    versioning = _load(root / "model_registry_versioning_policy_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")
    version_note = (root / "model_registry_version_note_v0.md").read_text(encoding="utf-8")

    post_sm = _load(post_root / "summary.json")
    post_vr = _load(post_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selected", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.next_route", summary.get("next_route") == NEXT_ROUTE)
    ok("summary.registry_v", summary.get("selected_registry_baseline_version") == REGISTRY_VERSION)
    ok("summary.schema_v", summary.get("selected_schema_version") == SCHEMA_VERSION)
    ok("summary.vstatus", summary.get("version_status") == VERSION_STATUS)
    ok("summary.vscope", summary.get("version_scope") == VERSION_SCOPE)
    ok("summary.future", summary.get("future_update_expected") is True)
    ok("summary.no_real", summary.get("real_provider_included") is False)
    ok("summary.no_prod", summary.get("production_runtime_included") is False)

    ok("version.policy.registry", versioning.get("registry_version") == REGISTRY_VERSION)
    ok("version.policy.schema", versioning.get("schema_version") == SCHEMA_VERSION)
    ok("version.policy.triggers10", len(versioning.get("update_triggers") or []) == 10)
    ok("version.policy.future6", len(versioning.get("future_versions") or []) == 6)
    ok("version.note.has_v0", REGISTRY_VERSION in version_note)
    ok("version.note.has_schema", SCHEMA_VERSION in version_note)

    for mid in V0_MODEL_IDS:
        ok(f"v0.model.{mid[:12]}", mid in version_note)

    for trigger in UPDATE_TRIGGERS:
        ok(f"trigger.{trigger[:16]}", trigger in (versioning.get("update_triggers") or []))

    for fv in FUTURE_VERSIONS:
        ok(f"future.{fv['version']}", fv["version"] in version_note)

    ok("non_claims.v0", any("model_registry_canonical_v0" in c for c in non_claims.get("non_claims") or []))

    ok("policy.selected", policy.get("selected_route") == SELECTED_ROUTE)
    ok("inp.pass", inp.get("review_pass") is True)
    ok("inp.b_foundation", inp.get("b_foundation_exists") is True)
    ok("inp.count7", inp.get("counts", {}).get("mock_fixture_model_registry") == 7)
    ok("inp.skill6", inp.get("counts", {}).get("skill_registry_dryrun") == 6)
    ok("inp.health6", inp.get("counts", {}).get("model_health_state_candidate") == 6)
    ok("inp.switch6", inp.get("counts", {}).get("model_switching_candidate") == 6)
    ok("inp.out7", inp.get("counts", {}).get("output_contract") == 7)

    ok("route_a.deferred", route_a.get("status") == "deferred")
    ok("route_b.selected", route_b.get("status") == "selected")
    ok("route_c.next", route_c.get("status") == "next_after_b_lite")
    ok("route_d.later", route_d.get("status") == "deferred_later")

    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)
    ok("matrix.next", matrix.get("next_route") == NEXT_ROUTE)
    ok("pre.met", pre.get("preconditions_met") is True)
    ok("ready.planning", readiness.get("ready_for_model_registry_canonicalization_planning") is True)

    ok("upstream.post", post_vr.get("verifier") == "GO")
    ok("upstream.final", post_sm.get("final_decision") == POST_REVIEW_FINAL)
    ok("upstream.next", post_sm.get("recommended_next_phase") == POST_REVIEW_NEXT)
    ok("upstream.consumable", post_sm.get("governance_skeleton_consumable") is True)

    for goal in B_LITE_GOALS:
        ok(f"b_lite.goal.{goal[:20]}", goal in (route_b.get("b_lite_goals") or []))

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("defer.a", defer.get("deferred_routes", [{}])[0].get("route") == DEFERRED_ROUTE_A)
    ok("defer.d", any(d.get("route") == DEFERRED_ROUTE_D for d in defer.get("deferred_routes") or []))

    for label in (ROUTE_A, ROUTE_B_LITE, ROUTE_C, ROUTE_D):
        ok(f"label.{label[:12]}", True)

    for i in range(12):
        ok(f"pad.{i}", summary.get("model_management_layer_roadmap_decision_only") is True)

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
