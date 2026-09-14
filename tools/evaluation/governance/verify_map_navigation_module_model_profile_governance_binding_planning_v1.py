#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Map / Navigation Module Model Profile + Governance Binding Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.asr_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as ASR_DR_FINAL_GO,
)
from capabilities.governance.first_person_scene_understanding_output_chain_closure_review_v1 import (
    FINAL_DECISION_GO as SCENE_CLOSURE_FINAL_GO,
)
from capabilities.governance.map_navigation_module_model_profile_governance_binding_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CLOSURE_CAN_SAY,
    CLOSURE_CANNOT_SAY,
    FINAL_DECISION_GO,
    IO_FORBIDDEN,
    MAP_NAV_MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    MAP_NAV_REGISTRY_REFS,
    MIDPLATFORM_BINDING_ID,
    MODULE_ID,
    MODULE_LOCAL_PROFILE_ID,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    QUALIFICATION_FIELDS,
    REUSED_GOVERNANCE_STANDARDS,
    SCOPE,
)
from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    CONSTITUTION_BUS_REF,
    CONTROLLED_RUNTIME_FRAMEWORK_REF,
    INFORMATION_INTEGRATION_REF,
    MODULE_LOCAL_PROFILE_STANDARD_REF,
    PROVIDER_ABS_STANDARD_ID,
    REGISTRY_REF,
    STANDARD_ID as MIDPLATFORM_BINDING_STANDARD_ID,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    DUAL_VALIDATION_MECHANISM_ID,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
)
from capabilities.governance.ocr_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as OCR_DR_FINAL_GO,
)
from capabilities.governance.tts_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as TTS_DR_FINAL_GO,
)
from capabilities.governance.vision_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VISION_DR_FINAL_GO,
)
from capabilities.governance.vision_module_model_profile_governance_binding_planning_v1 import (
    QUALIFICATION_CHECK_CRITERIA,
    QUALIFICATION_MODE,
)

MIN_CHECKS = 236

REQUIRED = (
    "map_navigation_module_model_profile_governance_binding_planning_policy_v1.json",
    "upstream_asr_module_input_review_v1.json",
    "governance_standard_reuse_review_v1.json",
    "map_navigation_module_definition_v1.json",
    "map_navigation_capability_stack_definition_v1.json",
    "map_navigation_layered_governance_mapping_v1.json",
    "map_navigation_module_local_model_profile_v1.json",
    "map_navigation_model_profile_registry_refs_review_v1.json",
    "map_navigation_model_role_assignment_plan_v1.json",
    "map_navigation_input_contract_v1.json",
    "map_navigation_output_contract_v1.json",
    "map_navigation_quality_acceptance_plan_v1.json",
    "map_navigation_health_validation_whitebox_plan_v1.json",
    "map_navigation_provider_runtime_boundary_plan_v1.json",
    "map_navigation_fallback_replacement_plan_v1.json",
    "map_navigation_module_internal_self_check_plan_v1.json",
    "map_navigation_midplatform_interaction_check_plan_v1.json",
    "map_navigation_midplatform_governance_binding_v1.json",
    "map_navigation_information_integration_handoff_plan_v1.json",
    "map_navigation_decision_center_handoff_plan_v1.json",
    "map_navigation_action_gate_boundary_plan_v1.json",
    "map_navigation_memory_worldmodel_admission_boundary_plan_v1.json",
    "map_navigation_layer_dependency_review_v1.json",
    "map_navigation_module_qualification_check_v1.json",
    "map_navigation_non_runtime_boundary_matrix_v1.json",
    "map_navigation_module_model_profile_governance_binding_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "map_navigation_module_model_profile_governance_binding_planning_decision_v1.json",
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
            "map_navigation_module_model_profile_governance_binding_planning"
        ),
    )
    p.add_argument(
        "--asr-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "asr_module_model_profile_governance_binding_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--tts-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "tts_module_model_profile_governance_binding_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--ocr-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_module_model_profile_governance_binding_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--vision-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "vision_module_model_profile_governance_binding_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--scene-closure-root",
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

    asr_dr_vr = _load(Path(args.asr_dryrun_root) / "verifier_report.json")
    asr_dr_sm = _load(Path(args.asr_dryrun_root) / "summary.json")
    tts_dr_vr = _load(Path(args.tts_dryrun_root) / "verifier_report.json")
    tts_dr_sm = _load(Path(args.tts_dryrun_root) / "summary.json")
    ocr_dr_vr = _load(Path(args.ocr_dryrun_root) / "verifier_report.json")
    ocr_dr_sm = _load(Path(args.ocr_dryrun_root) / "summary.json")
    vision_dr_vr = _load(Path(args.vision_dryrun_root) / "verifier_report.json")
    vision_dr_sm = _load(Path(args.vision_dryrun_root) / "summary.json")
    scene_closure_vr = _load(Path(args.scene_closure_root) / "verifier_report.json")
    scene_closure_sm = _load(Path(args.scene_closure_root) / "summary.json")

    ok("upstream.asr_go", asr_dr_vr.get("verifier") == "GO")
    ok("upstream.asr_final", asr_dr_sm.get("final_decision") == ASR_DR_FINAL_GO)
    ok("upstream.tts_go", tts_dr_vr.get("verifier") == "GO")
    ok("upstream.tts_final", tts_dr_sm.get("final_decision") == TTS_DR_FINAL_GO)
    ok("upstream.ocr_go", ocr_dr_vr.get("verifier") == "GO")
    ok("upstream.ocr_final", ocr_dr_sm.get("final_decision") == OCR_DR_FINAL_GO)
    ok("upstream.vision_go", vision_dr_vr.get("verifier") == "GO")
    ok("upstream.vision_final", vision_dr_sm.get("final_decision") == VISION_DR_FINAL_GO)
    ok("upstream.scene_go", scene_closure_vr.get("verifier") == "GO")
    ok("upstream.scene_final", scene_closure_sm.get("final_decision") == SCENE_CLOSURE_FINAL_GO)

    summary = _load(root / "summary.json")
    policy = _load(root / "map_navigation_module_model_profile_governance_binding_planning_policy_v1.json")
    upstream = _load(root / "upstream_asr_module_input_review_v1.json")
    gov_reuse = _load(root / "governance_standard_reuse_review_v1.json")
    mod_def = _load(root / "map_navigation_module_definition_v1.json")
    stack = _load(root / "map_navigation_capability_stack_definition_v1.json")
    gov_map = _load(root / "map_navigation_layered_governance_mapping_v1.json")
    profile = _load(root / "map_navigation_module_local_model_profile_v1.json")
    refs_review = _load(root / "map_navigation_model_profile_registry_refs_review_v1.json")
    roles = _load(root / "map_navigation_model_role_assignment_plan_v1.json")
    inp = _load(root / "map_navigation_input_contract_v1.json")
    out = _load(root / "map_navigation_output_contract_v1.json")
    quality = _load(root / "map_navigation_quality_acceptance_plan_v1.json")
    health = _load(root / "map_navigation_health_validation_whitebox_plan_v1.json")
    prov_rt = _load(root / "map_navigation_provider_runtime_boundary_plan_v1.json")
    fallback = _load(root / "map_navigation_fallback_replacement_plan_v1.json")
    self_check = _load(root / "map_navigation_module_internal_self_check_plan_v1.json")
    interaction = _load(root / "map_navigation_midplatform_interaction_check_plan_v1.json")
    binding = _load(root / "map_navigation_midplatform_governance_binding_v1.json")
    ii = _load(root / "map_navigation_information_integration_handoff_plan_v1.json")
    dc = _load(root / "map_navigation_decision_center_handoff_plan_v1.json")
    action_gate = _load(root / "map_navigation_action_gate_boundary_plan_v1.json")
    mem_wm = _load(root / "map_navigation_memory_worldmodel_admission_boundary_plan_v1.json")
    layer_dep = _load(root / "map_navigation_layer_dependency_review_v1.json")
    boundary = _load(root / "map_navigation_non_runtime_boundary_matrix_v1.json")
    qual = _load(root / "map_navigation_module_qualification_check_v1.json")
    dryrun = _load(root / "map_navigation_module_model_profile_governance_binding_dryrun_plan_v1.json")
    decision = _load(root / "map_navigation_module_model_profile_governance_binding_planning_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.module", summary.get("module_id") == MODULE_ID)
    ok("summary.layer3", summary.get("capability_layer") == "Layer 3 Navigation Application")
    ok("summary.refs4", summary.get("registry_model_profile_ref_count") == 4)
    ok("summary.qual_mode", summary.get("qualification_mode") == QUALIFICATION_MODE)
    ok("summary.qual_only", summary.get("qualification_check_only") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.registry", summary.get("registry_ref") == REGISTRY_REF)
    ok("summary.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.qual_only", policy.get("qualification_check_only") is True)
    ok("policy.layer3", "Layer 3 application layer" in (policy.get("phase_goal") or ""))
    ok("upstream.pass", upstream.get("review_pass") is True)

    ok(
        "gov_reuse.not_framework",
        gov_reuse.get("map_navigation_module_qualification_planning_not_new_framework") is True,
    )
    for std in REUSED_GOVERNANCE_STANDARDS:
        ok(f"gov_reuse.{std[:16]}", std in (gov_reuse.get("reused_standards") or []))

    ok("mod_def.id", mod_def.get("module_id") == MODULE_ID)
    ok("mod_def.layer3", mod_def.get("capability_layer") == "Layer 3 Navigation Application")
    ok("mod_def.l1", mod_def.get("depends_on_layer_1") == "Current Scene Understanding")
    ok("mod_def.l2", mod_def.get("depends_on_layer_2") == "Spatiotemporal Continuity")
    ok("mod_def.no_provider", mod_def.get("map_provider_invoked_now") is False)
    ok("mod_def.no_route", mod_def.get("route_planning_executed_now") is False)
    ok("mod_def.no_action", mod_def.get("navigation_action_generated_now") is False)
    ok("mod_def.candidate", mod_def.get("candidate_only") is True)
    mod_text = json.dumps(mod_def, ensure_ascii=False)
    ok("mod_def.no_override_l1", "cannot override Layer 1" in mod_text)

    stack_text = json.dumps(stack, ensure_ascii=False)
    ok("stack.l1", "scene_context_candidate_ref" in stack_text)
    ok("stack.l2", "location_context_candidate" in stack_text)
    ok("stack.l3", "route_context_candidate" in stack_text)
    ok("stack.l4", "indoor_navigation_candidate_later" in stack_text)
    ok("stack.no_action", "no direct navigation action" in stack_text)

    gov_text = json.dumps(gov_map, ensure_ascii=False)
    ok("gov.l1", "cannot override perception" in gov_text)
    ok("gov.l2", "conflict/gap/freshness required" in gov_text)
    ok("gov.l3", "Navigation Action Gate later" in gov_text)
    ok("gov.safety", "survival safety overrides task progress" in gov_text)

    ok("profile.id", profile.get("module_local_profile_id") == MODULE_LOCAL_PROFILE_ID)
    ok("profile.health_later", profile.get("health_requirement_ref") == "required_later")
    ok("profile.no_nav_action", profile.get("no_direct_navigation_action") is True)
    ok("profile.no_user_out", profile.get("no_direct_user_output") is True)
    for ref in MAP_NAV_REGISTRY_REFS:
        ok(f"profile.ref.{ref[:12]}", ref in (profile.get("registry_model_profile_refs") or []))

    ok("refs.pass", refs_review.get("review_pass") is True)
    ok("refs.map_provider", "map_provider_placeholder_candidate" in json.dumps(refs_review))
    ok("refs.route", "route_reasoning_candidate" in json.dumps(refs_review))
    ok("refs.facility", "indoor_facility_search_candidate" in json.dumps(refs_review))
    ok("refs.transit", "transit_context_candidate" in json.dumps(refs_review))

    roles_text = json.dumps(roles, ensure_ascii=False)
    ok("roles.map", "map context provider role" in roles_text)
    ok("roles.route", "route proposal role" in roles_text)
    ok("roles.not_permission", "route candidate ≠ navigation permission" in roles_text)

    inp_text = json.dumps(inp, ensure_ascii=False)
    ok("inp.no_map_api", "map API not called now" in inp_text)
    ok("inp.no_location_fact", "real location fact not generated now" in inp_text)

    out_text = json.dumps(out, ensure_ascii=False)
    ok("out.route_ctx", "route_context_candidate" in out_text)
    for forbidden in IO_FORBIDDEN:
        ok(f"out.forbid.{forbidden[:14]}", forbidden in (out.get("forbidden_outputs") or []))

    ok("quality.benchmark_now", quality.get("benchmark_executed_now") is False)
    ok("quality.compliance", quality.get("candidate_contract_compliance_required") is True)

    ok("health.health_later", health.get("health_requirement_ref") == "required_later")
    ok("health.detail_false", health.get("health_metric_detail_defined_now") is False)
    ok("health.transport", health.get("health_status_ref_transport_only") is True)
    ok("health.freshness_later", health.get("map_source_freshness_trace_required_later") is True)

    ok("prov.no_runtime", "Map / Navigation runtime remains disabled now" in json.dumps(prov_rt))
    ok("prov.abstraction", prov_rt.get("provider_abstraction_required") is True)

    ok("binding.id", binding.get("midplatform_governance_binding_id") == MIDPLATFORM_BINDING_ID)
    ok("binding.ii", bool(binding.get("information_integration_consumption_policy_ref")))
    ok("binding.dc", bool(binding.get("decision_center_consumption_policy_ref")))
    ok("binding.nav_gate", bool(binding.get("navigation_action_gate_requirement_ref_later")))
    ok("binding.constitution", binding.get("constitution_bus_ref") == CONSTITUTION_BUS_REF)
    ok("binding.no_runtime", binding.get("runtime_enabled_now") is False)

    ii_text = json.dumps(ii, ensure_ascii=False)
    ok("ii.no_bypass", "cannot bypass Information Integration" in ii_text)

    dc_text = json.dumps(dc, ensure_ascii=False)
    ok("dc.no_movement", "cannot emit final movement decision" in dc_text)
    ok("dc.no_route_action", "route candidate cannot directly trigger navigation action" in dc_text)

    action_text = json.dumps(action_gate, ensure_ascii=False)
    ok("action.gate_required", "Navigation Action Gate required later" in action_text)
    ok("action.no_go_ahead", "safe_to_cross / go_ahead forbidden now" in action_text)

    mem_text = json.dumps(mem_wm, ensure_ascii=False)
    ok("mem.no_write", "cannot write Memory" in mem_text)

    layer_text = json.dumps(layer_dep, ensure_ascii=False)
    ok("layer.l1_dep", "depends on Layer 1 scene understanding" in layer_text)
    ok("layer.no_override", "cannot override safety/risk candidates" in layer_text)

    ok("boundary.all_false", boundary.get("all_false") is True)

    ok("qual.pass", qual.get("qualification_pass") is True)
    ok("qual.criteria8", qual.get("criteria_count") == len(QUALIFICATION_CHECK_CRITERIA))
    for k, v in QUALIFICATION_FIELDS.items():
        ok(f"qual.field.{k[:18]}", (qual.get("qualification_fields") or {}).get(k) is v)
    for item in CLOSURE_CAN_SAY:
        ok(f"qual.can.{item[:16]}", item in (qual.get("can_say") or []))
    for item in CLOSURE_CANNOT_SAY:
        ok(f"qual.cannot.{item[:16]}", item in (qual.get("cannot_say") or []))

    ok("decision.qual_only", decision.get("qualification_check_only") is True)
    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("dryrun.qual", dryrun.get("qualification_mode") == QUALIFICATION_MODE)
    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    for claim in NON_CLAIMS:
        ok(
            f"non_claim.{claim[:18]}",
            claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []),
        )

    for item in MODULE_INTERNAL_SELF_CHECK_COVERAGE:
        ok(f"self_check.{item[:16]}", item in (self_check.get("self_check_coverage") or []))
    for item in MAP_NAV_MIDPLATFORM_INTERACTION_CHECK_COVERAGE:
        ok(f"interaction.{item[:16]}", item in (interaction.get("interaction_check_coverage") or []))

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
        "qualification_mode": QUALIFICATION_MODE,
        "module_id": MODULE_ID,
        "capability_layer": "Layer 3 Navigation Application",
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    if verifier != "GO":
        failed = [c["check_id"] for c in checks if not c["passed"]]
        print(json.dumps({"failed_checks": failed[:25]}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
