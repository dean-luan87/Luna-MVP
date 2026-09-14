#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision Module Model Profile + Governance Binding Planning v1."""

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
    FINAL_DECISION_GO as FP_SCENE_CLOSURE_FINAL_GO,
)
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import SYSTEM_ID as GATE_CHAIN_SYSTEM_ID
from capabilities.governance.midplatform_model_governance_binding_standardization_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as BINDING_DR_FINAL_GO,
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
    DUAL_VALIDATION_NON_CLAIMS,
    MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
)
from capabilities.governance.vision_module_model_profile_governance_binding_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CLOSURE_CAN_SAY,
    CLOSURE_CANNOT_SAY,
    FINAL_DECISION_GO,
    IO_FORBIDDEN,
    MIDPLATFORM_BINDING_ID,
    MODULE_ID,
    MODULE_LOCAL_PROFILE_ID,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    QUALIFICATION_CHECK_CRITERIA,
    QUALIFICATION_FIELDS,
    QUALIFICATION_MODE,
    REUSED_GOVERNANCE_STANDARDS,
    SCOPE,
    VISION_REGISTRY_REFS,
)

MIN_CHECKS = 273

REQUIRED = (
    "vision_module_model_profile_governance_binding_planning_policy_v1.json",
    "upstream_binding_standard_input_review_v1.json",
    "governance_standard_reuse_review_v1.json",
    "vision_module_definition_v1.json",
    "vision_capability_stack_definition_v1.json",
    "vision_layered_governance_mapping_v1.json",
    "vision_module_local_model_profile_v1.json",
    "vision_model_profile_registry_refs_review_v1.json",
    "vision_model_role_assignment_plan_v1.json",
    "vision_input_contract_v1.json",
    "vision_output_contract_v1.json",
    "vision_quality_acceptance_plan_v1.json",
    "vision_health_validation_whitebox_plan_v1.json",
    "vision_provider_runtime_boundary_plan_v1.json",
    "vision_fallback_replacement_plan_v1.json",
    "vision_module_internal_self_check_plan_v1.json",
    "vision_midplatform_interaction_check_plan_v1.json",
    "vision_midplatform_governance_binding_v1.json",
    "vision_information_integration_handoff_plan_v1.json",
    "vision_decision_center_handoff_plan_v1.json",
    "vision_gate_chain_boundary_plan_v1.json",
    "vision_memory_worldmodel_admission_boundary_plan_v1.json",
    "vision_non_runtime_boundary_matrix_v1.json",
    "vision_module_qualification_check_v1.json",
    "vision_module_model_profile_governance_binding_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "vision_module_model_profile_governance_binding_planning_decision_v1.json",
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
            "vision_module_model_profile_governance_binding_planning"
        ),
    )
    p.add_argument(
        "--binding-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_model_governance_binding_standardization_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--fp-closure-root",
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

    binding_dr_vr = _load(Path(args.binding_dryrun_root) / "verifier_report.json")
    binding_dr_sm = _load(Path(args.binding_dryrun_root) / "summary.json")
    fp_sm = _load(Path(args.fp_closure_root) / "summary.json")

    ok("upstream.binding_go", binding_dr_vr.get("verifier") == "GO")
    ok("upstream.binding_final", binding_dr_sm.get("final_decision") == BINDING_DR_FINAL_GO)
    ok("upstream.fp_closure", fp_sm.get("final_decision") == FP_SCENE_CLOSURE_FINAL_GO)

    summary = _load(root / "summary.json")
    policy = _load(root / "vision_module_model_profile_governance_binding_planning_policy_v1.json")
    upstream = _load(root / "upstream_binding_standard_input_review_v1.json")
    gov_reuse = _load(root / "governance_standard_reuse_review_v1.json")
    mod_def = _load(root / "vision_module_definition_v1.json")
    stack = _load(root / "vision_capability_stack_definition_v1.json")
    gov_map = _load(root / "vision_layered_governance_mapping_v1.json")
    profile = _load(root / "vision_module_local_model_profile_v1.json")
    refs_review = _load(root / "vision_model_profile_registry_refs_review_v1.json")
    roles = _load(root / "vision_model_role_assignment_plan_v1.json")
    inp = _load(root / "vision_input_contract_v1.json")
    out = _load(root / "vision_output_contract_v1.json")
    quality = _load(root / "vision_quality_acceptance_plan_v1.json")
    health = _load(root / "vision_health_validation_whitebox_plan_v1.json")
    prov_rt = _load(root / "vision_provider_runtime_boundary_plan_v1.json")
    fallback = _load(root / "vision_fallback_replacement_plan_v1.json")
    self_check = _load(root / "vision_module_internal_self_check_plan_v1.json")
    interaction = _load(root / "vision_midplatform_interaction_check_plan_v1.json")
    binding = _load(root / "vision_midplatform_governance_binding_v1.json")
    ii = _load(root / "vision_information_integration_handoff_plan_v1.json")
    dc = _load(root / "vision_decision_center_handoff_plan_v1.json")
    gate = _load(root / "vision_gate_chain_boundary_plan_v1.json")
    mem_wm = _load(root / "vision_memory_worldmodel_admission_boundary_plan_v1.json")
    boundary = _load(root / "vision_non_runtime_boundary_matrix_v1.json")
    dryrun = _load(root / "vision_module_model_profile_governance_binding_dryrun_plan_v1.json")
    decision = _load(root / "vision_module_model_profile_governance_binding_planning_decision_v1.json")
    qual = _load(root / "vision_module_qualification_check_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.qual_mode", summary.get("qualification_mode") == QUALIFICATION_MODE)
    ok("summary.qual_only", summary.get("qualification_check_only") is True)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.module", summary.get("module_id") == MODULE_ID)
    ok("summary.refs4", summary.get("registry_model_profile_ref_count") == 4)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.registry", summary.get("registry_ref") == REGISTRY_REF)
    ok("summary.binding_std", summary.get("midplatform_binding_standard_ref") == MIDPLATFORM_BINDING_STANDARD_ID)
    ok("summary.ml_std", summary.get("module_local_profile_standard_ref") == MODULE_LOCAL_PROFILE_STANDARD_REF)
    ok("summary.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("summary.deferred", summary.get("non_compliant_module_model_handling_policy_deferred") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.qual_only", policy.get("qualification_check_only") is True)
    ok("policy.goal", "qualification" in str(policy.get("phase_goal", "")).lower())
    ok("upstream.pass", upstream.get("review_pass") is True)
    ok("upstream.deferred", upstream.get("non_compliant_module_model_handling_policy_deferred") is True)

    ok("gov_reuse.ref", gov_reuse.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("gov_reuse.not_framework", gov_reuse.get("vision_module_planning_not_new_framework") is True)
    for std in REUSED_GOVERNANCE_STANDARDS:
        ok(f"gov_reuse.{std[:16]}", std in (gov_reuse.get("reused_standards") or []))

    ok("mod_def.id", mod_def.get("module_id") == MODULE_ID)
    ok("mod_def.type", mod_def.get("module_type") == "pluggable_capability_module")
    ok("mod_def.domain", "First-Person Vision" in mod_def.get("capability_domain", ""))
    ok("mod_def.primary", mod_def.get("primary_goal") == "Current Scene Understanding")
    ok("mod_def.no_runtime", mod_def.get("runtime_enabled_now") is False)
    ok("mod_def.candidate", mod_def.get("candidate_only") is True)
    mod_text = json.dumps(mod_def, ensure_ascii=False)
    ok("mod_def.no_nav", "navigation action" in mod_text)
    ok("mod_def.no_fact", "fact" in mod_text)
    ok("mod_def.ii", "Information Integration" in mod_text)

    stack_text = json.dumps(stack, ensure_ascii=False)
    ok("stack.id", stack.get("definition_id") == "vision_capability_stack_definition_v1")
    ok("stack.l1_obs", "visual_observation_candidate" in stack_text)
    ok("stack.l1_target", "target_recognition_candidate" in stack_text)
    ok("stack.l1_scene", "scene_context_candidate" in stack_text)
    ok("stack.l1_risk", "risk_context_candidate" in stack_text)
    ok("stack.l1_text", "text_region_need_candidate" in stack_text)
    ok("stack.l2_track", "target_tracking_candidate" in stack_text)
    ok("stack.l3_route", "route_visual_context_candidate" in stack_text)
    ok("stack.no_nav", "no direct navigation action" in stack_text)

    gov_text = json.dumps(gov_map, ensure_ascii=False)
    ok("gov_map.id", gov_map.get("mapping_id") == "vision_layered_governance_mapping_v1")
    ok("gov_map.l1_source", "source_chain" in gov_text)
    ok("gov_map.l1_not_fact", "not_fact" in gov_text)
    ok("gov_map.l2_fresh", "freshness" in gov_text)
    ok("gov_map.l3_safety", "safety context" in gov_text)
    ok("gov_map.l4_privacy", "privacy/identity gates later" in gov_text)
    ok("gov_map.no_overload", "no all-rules-to-all-layers overload" in gov_text)

    ok("profile.id", profile.get("module_local_profile_id") == MODULE_LOCAL_PROFILE_ID)
    ok("profile.module", profile.get("module_id") == MODULE_ID)
    ok("profile.stack", profile.get("capability_stack_ref") == "vision_capability_stack_definition_v1")
    ok("profile.gov", profile.get("layered_governance_mapping_ref") == "vision_layered_governance_mapping_v1")
    ok("profile.health_later", profile.get("health_requirement_ref") == "required_later")
    ok("profile.supervision_later", profile.get("supervision_metric_ref") == "required_later")
    ok("profile.no_override", profile.get("no_registry_override") is True)
    ok("profile.no_select", profile.get("no_model_selection_by_module") is True)
    ok("profile.no_invoke", profile.get("no_model_invocation_by_profile") is True)
    ok("profile.no_fact", profile.get("no_direct_fact_action_output") is True)
    for ref in VISION_REGISTRY_REFS:
        ok(f"profile.ref.{ref[:12]}", ref in (profile.get("registry_model_profile_refs") or []))

    ok("refs.pass", refs_review.get("review_pass") is True)
    ok("refs.count4", len(refs_review.get("registry_model_profile_refs") or []) == 4)

    roles_text = json.dumps(roles, ensure_ascii=False)
    ok("roles.yolo", "object_detection_candidate" in roles_text)
    ok("roles.grounded", "grounding/segmentation later" in roles_text)
    ok("roles.tracking", "temporal target tracking later" in roles_text)
    ok("roles.vlm", "scene understanding candidate later" in roles_text)
    ok("roles.no_brain", "no universal vision brain" in roles_text)

    inp_text = json.dumps(inp, ensure_ascii=False)
    ok("inp.frame_later", "frame_candidate_later" in inp_text)
    ok("inp.no_real_frame", "real_frame input not allowed now" in inp_text)
    ok("inp.no_camera", "camera source not invoked now" in inp_text)
    ok("inp.cr_later", "Controlled Runtime later" in inp_text)

    out_text = json.dumps(out, ensure_ascii=False)
    ok("out.obs", "visual_observation_candidate" in out_text)
    ok("out.evidence", "visual_evidence_candidate" in out_text)
    for forbidden in IO_FORBIDDEN:
        ok(f"out.forbid.{forbidden[:14]}", forbidden in (out.get("forbidden_outputs") or []))

    ok("quality.benchmark_later", quality.get("benchmark_required_later") is True)
    ok("quality.benchmark_now", quality.get("benchmark_executed_now") is False)
    ok("quality.compliance", quality.get("candidate_contract_compliance_required") is True)

    ok("health.health_later", health.get("health_requirement_ref") == "required_later")
    ok("health.supervision_later", health.get("supervision_metric_ref") == "required_later")
    ok("health.detail_false", health.get("health_metric_detail_defined_now") is False)
    ok("health.super_detail_false", health.get("supervision_metric_detail_defined_now") is False)
    ok("health.evidence", health.get("evidence_refs_required") is True)
    ok("health.no_self", health.get("module_cannot_self_certify_health") is True)

    prov_text = json.dumps(prov_rt, ensure_ascii=False)
    ok("prov.required", prov_rt.get("provider_abstraction_required") is True)
    ok("prov.cr_required", prov_rt.get("controlled_runtime_required") is True)
    ok("prov.no_runtime", "Vision runtime remains disabled now" in prov_text)

    ok("fallback.refs", len(fallback.get("fallback_model_profile_refs") or []) == 4)
    ok("fallback.conditions6", len(fallback.get("replacement_conditions") or []) >= 6)
    ok("fallback.no_auto", fallback.get("no_auto_switch_without_governance_policy") is True)

    ok("self_check.dual", self_check.get("dual_validation_mechanism_ref") == DUAL_VALIDATION_MECHANISM_ID)
    for item in MODULE_INTERNAL_SELF_CHECK_COVERAGE:
        ok(f"self_check.{item[:16]}", item in (self_check.get("self_check_coverage") or []))

    ok("interaction.dual", interaction.get("dual_validation_mechanism_ref") == DUAL_VALIDATION_MECHANISM_ID)
    for item in MIDPLATFORM_INTERACTION_CHECK_COVERAGE:
        ok(f"interaction.{item[:16]}", item in (interaction.get("interaction_check_coverage") or []))

    ok("binding.id", binding.get("midplatform_governance_binding_id") == MIDPLATFORM_BINDING_ID)
    ok("binding.profile", binding.get("module_local_profile_ref") == MODULE_LOCAL_PROFILE_ID)
    ok("binding.constitution", binding.get("constitution_bus_ref") == CONSTITUTION_BUS_REF)
    ok("binding.provider", binding.get("provider_abstraction_ref") == PROVIDER_ABS_STANDARD_ID)
    ok("binding.cr", binding.get("controlled_runtime_requirement_ref") == CONTROLLED_RUNTIME_FRAMEWORK_REF)
    ok("binding.no_select", binding.get("model_selected_now") is False)
    ok("binding.no_invoke", binding.get("model_invoked_now") is False)
    ok("binding.health_later", binding.get("health_requirement_ref") == "required_later")
    ok("binding.supervision_later", binding.get("supervision_metric_ref") == "required_later")

    ii_text = json.dumps(ii, ensure_ascii=False)
    ok("ii.ref", ii.get("information_integration_ref") == INFORMATION_INTEGRATION_REF)
    ok("ii.no_bypass", "cannot bypass Information Integration" in ii_text)
    ok("ii.no_integrated", "no integrated_context generated now" in ii_text)

    dc_text = json.dumps(dc, ensure_ascii=False)
    ok("dc.integrated", "integrated_context" in dc_text)
    ok("dc.no_decision", "no decision generated now" in dc_text)

    ok("gate.not_output", gate.get("output_capable_now") is False)
    ok("gate.ref", gate.get("gate_chain_system_ref") == GATE_CHAIN_SYSTEM_ID)

    mem_text = json.dumps(mem_wm, ensure_ascii=False)
    ok("mem.no_write", "cannot write Memory" in mem_text)
    ok("mem.no_wm", "cannot write WorldModel" in mem_text)

    ok("boundary.all_false", boundary.get("all_false") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:12]}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("dryrun.qual", dryrun.get("qualification_mode") == QUALIFICATION_MODE)
    ok("dryrun.qual_only", "qualification check only" in str(dryrun.get("objectives")).lower())
    ok("decision.pass", decision.get("planning_pass") is True)
    ok("binding.no_runtime", binding.get("runtime_enabled_now") is False)

    ok("qual.pass", qual.get("qualification_pass") is True)
    ok("qual.mode", qual.get("qualification_mode") == QUALIFICATION_MODE)
    ok("qual.criteria8", qual.get("criteria_count") == len(QUALIFICATION_CHECK_CRITERIA))
    for k, v in QUALIFICATION_FIELDS.items():
        ok(f"qual.field.{k[:18]}", qual.get("qualification_fields", {}).get(k) is v)
    for item in CLOSURE_CAN_SAY:
        ok(f"qual.can.{item[:16]}", item in (qual.get("can_say") or []))
    for item in CLOSURE_CANNOT_SAY:
        ok(f"qual.cannot.{item[:16]}", item in (qual.get("cannot_say") or []))

    ok("decision.qual_mode", decision.get("qualification_mode") == QUALIFICATION_MODE)
    ok("decision.qual_only", decision.get("qualification_check_only") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

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
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
