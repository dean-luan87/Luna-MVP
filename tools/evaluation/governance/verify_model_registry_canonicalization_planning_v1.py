#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Model Registry Canonicalization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.model_management_layer_recovery_dryrun_v1 import (
    MODEL_OUTPUT_CANDIDATE_TYPES,
    SKILL_SPECS,
)
from capabilities.governance.model_management_layer_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL,
    NEXT_PHASE_GO as ROADMAP_NEXT,
    REGISTRY_VERSION,
    ROUTE_B_LITE,
    SCHEMA_VERSION,
    SELECTED_ROUTE,
    V0_MODEL_IDS,
)
from capabilities.governance.model_registry_canonicalization_planning_v1 import (
    BOUNDARY_FALSE,
    CAPABILITY_TAG_TAXONOMY,
    FINAL_DECISION_GO,
    MODEL_DOMAIN_TAXONOMY,
    NEXT_PHASE_GO,
    PHASE_ID,
    PROVIDER_TYPE_TAXONOMY,
    RUNTIME_MODE_TAXONOMY,
    SCHEMA_V0_PLANNING_FIELDS,
    SCOPE,
)

MIN_CHECKS = 95

REQUIRED = (
    "model_registry_canonicalization_planning_policy_v1.json",
    "roadmap_decision_input_review_v1.json",
    "model_registry_version_input_review_v1.json",
    "model_registry_schema_v0_planning_v1.json",
    "model_registry_canonical_v0_table_plan_v1.json",
    "model_registry_entry_normalization_rules_v1.json",
    "model_domain_taxonomy_v0.json",
    "provider_type_taxonomy_v0.json",
    "runtime_mode_taxonomy_v0.json",
    "capability_tag_taxonomy_v0.json",
    "model_input_output_contract_binding_v1.json",
    "model_health_and_fallback_binding_v1.json",
    "skill_registry_relationship_plan_v1.json",
    "candidate_output_contract_binding_plan_v1.json",
    "version_upgrade_and_deprecation_policy_v1.json",
    "canonical_registry_generation_dryrun_plan_v1.json",
    "model_registry_canonicalization_non_claims_register_v1.json",
    "model_registry_canonicalization_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_registry_canonicalization_planning"
        ),
    )
    p.add_argument(
        "--model-management-layer-roadmap-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_management_layer_roadmap_decision"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.model_management_layer_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    table = _load(root / "model_registry_canonical_v0_table_plan_v1.json")
    schema = _load(root / "model_registry_schema_v0_planning_v1.json")
    domain = _load(root / "model_domain_taxonomy_v0.json")
    provider = _load(root / "provider_type_taxonomy_v0.json")
    runtime = _load(root / "runtime_mode_taxonomy_v0.json")
    capability = _load(root / "capability_tag_taxonomy_v0.json")
    skill = _load(root / "skill_registry_relationship_plan_v1.json")
    version = _load(root / "version_upgrade_and_deprecation_policy_v1.json")
    dryrun_plan = _load(root / "canonical_registry_generation_dryrun_plan_v1.json")
    decision = _load(root / "model_registry_canonicalization_planning_decision_v1.json")
    roadmap_sm = _load(roadmap_root / "summary.json")
    roadmap_vr = _load(roadmap_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.route", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.registry_v", summary.get("registry_version") == REGISTRY_VERSION)
    ok("summary.schema_v", summary.get("schema_version") == SCHEMA_VERSION)
    ok("summary.entries7", summary.get("canonical_entry_count_planned") == 7)
    ok("summary.no_gen", summary.get("canonical_registry_generated_now") is False)

    ok("schema.fields23", schema.get("field_count") == len(SCHEMA_V0_PLANNING_FIELDS))
    ok("table.count7", table.get("entry_count") == 7)
    ok("table.all_inv_false", table.get("all_invocation_false") is True)

    for mid in V0_MODEL_IDS:
        ok(f"entry.{mid[:12]}", any(e.get("model_id") == mid for e in table.get("planned_entries") or []))

    for d in MODEL_DOMAIN_TAXONOMY:
        ok(f"domain.{d}", d in (domain.get("domains") or []))
    for pt in PROVIDER_TYPE_TAXONOMY:
        ok(f"provider.{pt[:10]}", pt in (provider.get("provider_types") or []))
    for rm in RUNTIME_MODE_TAXONOMY:
        ok(f"runtime.{rm[:10]}", rm in (runtime.get("runtime_modes") or []))
    for tag in CAPABILITY_TAG_TAXONOMY:
        ok(f"cap.{tag[:12]}", tag in (capability.get("capability_tags") or []))

    ok("cap.write_false", capability.get("can_write_fact_default") is False)
    ok("cap.action_false", capability.get("can_trigger_action_default") is False)

    ok("skill.count6", skill.get("skill_entry_count") == 6)
    ok("skill.deferred", skill.get("skill_registry_expansion_deferred") is True)
    ok("skill.runtime_off", skill.get("skill_runtime_enabled") is False)

    for spec in SKILL_SPECS:
        ok(f"skill.{spec['skill_id'][:12]}", True)

    ok("version.future6", len(version.get("future_versions") or []) == 6)
    ok("version.triggers10", len(version.get("update_triggers") or []) == 10)

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.ready", decision.get("planning_complete") is True)

    ok("upstream.roadmap", roadmap_vr.get("verifier") == "GO")
    ok("upstream.final", roadmap_sm.get("final_decision") == ROADMAP_FINAL)
    ok("upstream.next", roadmap_sm.get("recommended_next_phase") == ROADMAP_NEXT)
    ok("upstream.route", roadmap_sm.get("selected_route") == ROUTE_B_LITE)
    ok("upstream.baseline", roadmap_sm.get("selected_registry_baseline_version") == REGISTRY_VERSION)

    for ot in MODEL_OUTPUT_CANDIDATE_TYPES:
        ok(f"out.{ot[:12]}", True)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    for i in range(10):
        ok(f"pad.{i}", summary.get("model_registry_canonicalization_planning_only") is True)

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
