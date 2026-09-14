#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Scenario Model Governance and Capability Roadmap Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.first_person_scene_understanding_output_chain_closure_review_v1 import (
    FINAL_DECISION_GO as CLOSURE_FINAL_GO,
)
from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.scenario_model_governance_and_capability_roadmap_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    GOAL_STAGES,
    IO_FORBIDDEN_OUTPUTS,
    IO_INPUT_TYPES,
    IO_OUTPUT_TYPES,
    MIDPLATFORM_BINDING_FIELDS,
    MODEL_SOURCE_TYPES,
    MODULE_PROFILE_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    ROADMAP_RISKS,
    SCENARIO_IDS,
    SCOPE,
    STAGE_CAPABILITIES,
)

MIN_CHECKS = 176

REQUIRED = (
    "scenario_model_roadmap_planning_policy_v1.json",
    "upstream_output_chain_input_review_v1.json",
    "luna_model_capability_roadmap_v1.json",
    "goal_stage_to_model_capability_matrix_v1.json",
    "model_source_strategy_taxonomy_v1.json",
    "external_open_source_candidate_register_v1.json",
    "reference_research_product_candidate_register_v1.json",
    "self_developed_core_capability_register_v1.json",
    "scene_model_requirement_matrix_v1.json",
    "module_local_model_profile_contract_v1.json",
    "midplatform_model_governance_binding_contract_v1.json",
    "model_input_output_contract_standard_v1.json",
    "model_supervision_requirement_matrix_v1.json",
    "model_quality_acceptance_criteria_v1.json",
    "model_versioning_and_update_policy_v1.json",
    "model_replacement_and_fallback_policy_v1.json",
    "model_to_capability_stack_mapping_v1.json",
    "model_to_governance_layer_mapping_v1.json",
    "first_person_scene_understanding_model_roadmap_v1.json",
    "spatiotemporal_world_continuity_model_roadmap_v1.json",
    "navigation_application_model_roadmap_v1.json",
    "extended_capability_model_roadmap_v1.json",
    "seed_core_and_evolution_model_boundary_v1.json",
    "roadmap_risk_register_v1.json",
    "roadmap_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "scenario_model_roadmap_planning_decision_v1.json",
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
            "scenario_model_governance_and_capability_roadmap_planning"
        ),
    )
    p.add_argument(
        "--closure-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_scene_understanding_output_chain_closure_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    closure_vr = _load(Path(args.closure_review_root) / "verifier_report.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "scenario_model_roadmap_planning_policy_v1.json")
    upstream = _load(root / "upstream_output_chain_input_review_v1.json")
    luna_roadmap = _load(root / "luna_model_capability_roadmap_v1.json")
    goal_matrix = _load(root / "goal_stage_to_model_capability_matrix_v1.json")
    source_tax = _load(root / "model_source_strategy_taxonomy_v1.json")
    external_reg = _load(root / "external_open_source_candidate_register_v1.json")
    reference_reg = _load(root / "reference_research_product_candidate_register_v1.json")
    self_dev = _load(root / "self_developed_core_capability_register_v1.json")
    scenario_matrix = _load(root / "scene_model_requirement_matrix_v1.json")
    module_contract = _load(root / "module_local_model_profile_contract_v1.json")
    mid_binding = _load(root / "midplatform_model_governance_binding_contract_v1.json")
    io_std = _load(root / "model_input_output_contract_standard_v1.json")
    supervision = _load(root / "model_supervision_requirement_matrix_v1.json")
    acceptance = _load(root / "model_quality_acceptance_criteria_v1.json")
    versioning = _load(root / "model_versioning_and_update_policy_v1.json")
    replacement = _load(root / "model_replacement_and_fallback_policy_v1.json")
    stack_map = _load(root / "model_to_capability_stack_mapping_v1.json")
    gov_map = _load(root / "model_to_governance_layer_mapping_v1.json")
    fp_roadmap = _load(root / "first_person_scene_understanding_model_roadmap_v1.json")
    st_roadmap = _load(root / "spatiotemporal_world_continuity_model_roadmap_v1.json")
    nav_roadmap = _load(root / "navigation_application_model_roadmap_v1.json")
    ext_roadmap = _load(root / "extended_capability_model_roadmap_v1.json")
    seed_boundary = _load(root / "seed_core_and_evolution_model_boundary_v1.json")
    risks = _load(root / "roadmap_risk_register_v1.json")
    dryrun_plan = _load(root / "roadmap_dryrun_plan_v1.json")
    decision = _load(root / "scenario_model_roadmap_planning_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("upstream.closure_go", closure_vr.get("verifier") == "GO")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.roadmap_only", policy.get("roadmap_planning_only_not_model_integration") is True)
    ok("upstream.pass", upstream.get("review_pass") is True)
    ok("upstream.stack_ref", upstream.get("layered_stack_standard_ref") == STANDARD_ID)
    ok("upstream.gov_ref", upstream.get("layered_governance_mapping_ref") == ADDENDUM_ID)

    ok("luna_roadmap.stages6", luna_roadmap.get("stage_count") == 6)
    ok("luna_roadmap.organs", "models are capability organs not Seed Core not Universal Brain" in (luna_roadmap.get("principles") or []))

    ok("goal_matrix.stages6", len(goal_matrix.get("stages") or []) == len(GOAL_STAGES))
    for stage in GOAL_STAGES:
        sid = stage["stage_id"]
        caps = next((s for s in (goal_matrix.get("stages") or []) if s.get("stage_id") == sid), {})
        ok(f"goal_matrix.{sid}", len(caps.get("required_capabilities") or []) == len(STAGE_CAPABILITIES[sid]))

    for st in MODEL_SOURCE_TYPES:
        ok(f"source_tax.{st[:12]}", st in (source_tax.get("source_types") or []))

    ok("external.register_only", external_reg.get("register_only") is True)
    ok("external.no_select", external_reg.get("no_model_selected") is True)
    ok("external.no_download", external_reg.get("no_download") is True)
    ok("external.no_benchmark", external_reg.get("no_benchmark_now") is True)
    ok("external.cats9", len(external_reg.get("candidates") or []) >= 9)

    ok("reference.not_dep", reference_reg.get("reference_not_dependency") is True)
    ok("reference.not_copy", reference_reg.get("inspired_by_not_copied") is True)
    ok("reference.refs8", len(reference_reg.get("references") or []) >= 8)

    ok("self_dev.count14", len(self_dev.get("capabilities") or []) >= 14)
    ok("self_dev.seed", "luna_seed_core" in (self_dev.get("capabilities") or []))

    ok("scenario.count10", len(scenario_matrix.get("scenarios") or []) == len(SCENARIO_IDS))
    for sid in SCENARIO_IDS:
        ok(
            f"scenario.{sid[:18]}",
            any(s.get("scenario_id") == sid for s in (scenario_matrix.get("scenarios") or [])),
        )

    ok("module_contract.fields", module_contract.get("field_count") == len(MODULE_PROFILE_FIELDS))
    for field in MODULE_PROFILE_FIELDS:
        ok(f"module_contract.{field[:12]}", field in (module_contract.get("required_fields") or []))

    ok("mid_binding.fields", mid_binding.get("field_count") == len(MIDPLATFORM_BINDING_FIELDS))
    ok("mid_binding.stack", mid_binding.get("layered_stack_ref") == STANDARD_ID)
    ok("mid_binding.gov", mid_binding.get("layered_governance_ref") == ADDENDUM_ID)

    for it in IO_INPUT_TYPES:
        ok(f"io.in.{it[:12]}", it in (io_std.get("input_types") or []))
    for ot in IO_OUTPUT_TYPES:
        ok(f"io.out.{ot[:12]}", ot in (io_std.get("output_types") or []))
    for fb in IO_FORBIDDEN_OUTPUTS:
        ok(f"io.forbid.{fb[:12]}", fb in (io_std.get("forbidden_outputs") or []))

    ok("supervision.count9", len(supervision.get("requirements") or []) >= 9)
    ok("acceptance.count13", len(acceptance.get("criteria") or []) >= 13)
    ok("versioning.fields15", len(versioning.get("fields") or []) >= 15)
    ok("replacement.no_auto", replacement.get("no_auto_switch_without_policy") is True)

    ok("stack_map.rules6", len(stack_map.get("rules") or []) >= 6)
    ok("gov_map.rules6", len(gov_map.get("rules") or []) >= 6)

    ok("fp_roadmap.stage1", fp_roadmap.get("goal_stage") == "stage_1")
    ok("fp_roadmap.roles8", len(fp_roadmap.get("model_roles") or []) >= 8)
    ok("st_roadmap.stage2", st_roadmap.get("goal_stage") == "stage_2")
    ok("st_roadmap.self_dev", any(r.get("source_strategy") == "self_developed_core_capability" for r in (st_roadmap.get("model_roles") or [])))
    ok("nav_roadmap.stage3", nav_roadmap.get("goal_stage") == "stage_3")
    ok("nav_roadmap.depends", "stage_1" in (nav_roadmap.get("depends_on") or []))
    ok("ext_roadmap.stage4", ext_roadmap.get("goal_stage") == "stage_4")
    ok("ext_roadmap.gates", "privacy_gate" in (ext_roadmap.get("requires_gates") or []))

    ok("seed_boundary.count7", len(seed_boundary.get("confirmations") or []) >= 7)
    ok("seed.not_replace", "Seed Core not replaceable by external model" in (seed_boundary.get("confirmations") or []))

    ok("risks.count12", risks.get("risk_count") == len(ROADMAP_RISKS))
    for risk in ROADMAP_RISKS:
        ok(f"risk.{risk[:18]}", risk in (risks.get("risks") or []))

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (non_claims.get("non_claims") or []))

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    min_checks = MIN_CHECKS if MIN_CHECKS else total
    verifier = "GO" if passed == total and passed >= min_checks else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": min_checks,
        "planning_pass": summary.get("planning_pass"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
