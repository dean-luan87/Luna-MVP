#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify World Continuity Module Model Profile + Governance Binding Planning v1."""

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
from capabilities.governance.first_person_scene_understanding_information_integration_chain_dryrun_v1 import (
    FINAL_DECISION_GO as II_CHAIN_DR_FINAL_GO,
)
from capabilities.governance.map_navigation_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MAP_NAV_DR_FINAL_GO,
)
from capabilities.governance.world_continuity_module_model_profile_governance_binding_planning_v1 import (
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
    QUALIFICATION_FIELDS,
    REUSED_GOVERNANCE_STANDARDS,
    SCOPE,
    STCM_REGISTRY_ID,
    WORLD_CONTINUITY_MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    WORLD_CONTINUITY_REGISTRY_REFS,
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
    "world_continuity_module_model_profile_governance_binding_planning_policy_v1.json",
    "upstream_map_navigation_module_input_review_v1.json",
    "governance_standard_reuse_review_v1.json",
    "world_continuity_module_definition_v1.json",
    "world_continuity_capability_stack_definition_v1.json",
    "world_continuity_layered_governance_mapping_v1.json",
    "world_continuity_module_local_model_profile_v1.json",
    "world_continuity_model_profile_registry_refs_review_v1.json",
    "world_continuity_model_role_assignment_plan_v1.json",
    "world_continuity_input_contract_v1.json",
    "world_continuity_output_contract_v1.json",
    "world_continuity_quality_acceptance_plan_v1.json",
    "world_continuity_health_validation_whitebox_plan_v1.json",
    "world_continuity_provider_runtime_boundary_plan_v1.json",
    "world_continuity_fallback_replacement_plan_v1.json",
    "world_continuity_module_internal_self_check_plan_v1.json",
    "world_continuity_midplatform_interaction_check_plan_v1.json",
    "world_continuity_midplatform_governance_binding_v1.json",
    "world_continuity_information_integration_handoff_plan_v1.json",
    "world_continuity_decision_center_handoff_plan_v1.json",
    "world_continuity_worldmodel_admission_boundary_plan_v1.json",
    "world_continuity_memory_admission_boundary_plan_v1.json",
    "world_continuity_layer_dependency_review_v1.json",
    "world_continuity_module_qualification_check_v1.json",
    "world_continuity_non_runtime_boundary_matrix_v1.json",
    "world_continuity_module_model_profile_governance_binding_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "world_continuity_module_model_profile_governance_binding_planning_decision_v1.json",
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
            "world_continuity_module_model_profile_governance_binding_planning"
        ),
    )
    p.add_argument(
        "--map-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "map_navigation_module_model_profile_governance_binding_dryrun_and_review"
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
        "--ii-chain-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_scene_understanding_information_integration_chain_dryrun"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    map_dr_vr = _load(Path(args.map_dryrun_root) / "verifier_report.json")
    map_dr_sm = _load(Path(args.map_dryrun_root) / "summary.json")
    asr_dr_vr = _load(Path(args.asr_dryrun_root) / "verifier_report.json")
    asr_dr_sm = _load(Path(args.asr_dryrun_root) / "summary.json")
    tts_dr_vr = _load(Path(args.tts_dryrun_root) / "verifier_report.json")
    tts_dr_sm = _load(Path(args.tts_dryrun_root) / "summary.json")
    ocr_dr_vr = _load(Path(args.ocr_dryrun_root) / "verifier_report.json")
    ocr_dr_sm = _load(Path(args.ocr_dryrun_root) / "summary.json")
    vision_dr_vr = _load(Path(args.vision_dryrun_root) / "verifier_report.json")
    vision_dr_sm = _load(Path(args.vision_dryrun_root) / "summary.json")
    ii_chain_vr = _load(Path(args.ii_chain_dryrun_root) / "verifier_report.json")
    ii_chain_sm = _load(Path(args.ii_chain_dryrun_root) / "summary.json")

    ok("upstream.map_go", map_dr_vr.get("verifier") == "GO")
    ok("upstream.map_final", map_dr_sm.get("final_decision") == MAP_NAV_DR_FINAL_GO)
    ok("upstream.asr_go", asr_dr_vr.get("verifier") == "GO")
    ok("upstream.asr_final", asr_dr_sm.get("final_decision") == ASR_DR_FINAL_GO)
    ok("upstream.tts_go", tts_dr_vr.get("verifier") == "GO")
    ok("upstream.tts_final", tts_dr_sm.get("final_decision") == TTS_DR_FINAL_GO)
    ok("upstream.ocr_go", ocr_dr_vr.get("verifier") == "GO")
    ok("upstream.ocr_final", ocr_dr_sm.get("final_decision") == OCR_DR_FINAL_GO)
    ok("upstream.vision_go", vision_dr_vr.get("verifier") == "GO")
    ok("upstream.vision_final", vision_dr_sm.get("final_decision") == VISION_DR_FINAL_GO)
    ok("upstream.ii_go", ii_chain_vr.get("verifier") == "GO")
    ok("upstream.ii_final", ii_chain_sm.get("final_decision") == II_CHAIN_DR_FINAL_GO)

    summary = _load(root / "summary.json")
    policy = _load(root / "world_continuity_module_model_profile_governance_binding_planning_policy_v1.json")
    upstream = _load(root / "upstream_map_navigation_module_input_review_v1.json")
    gov_reuse = _load(root / "governance_standard_reuse_review_v1.json")
    mod_def = _load(root / "world_continuity_module_definition_v1.json")
    stack = _load(root / "world_continuity_capability_stack_definition_v1.json")
    gov_map = _load(root / "world_continuity_layered_governance_mapping_v1.json")
    profile = _load(root / "world_continuity_module_local_model_profile_v1.json")
    refs_review = _load(root / "world_continuity_model_profile_registry_refs_review_v1.json")
    roles = _load(root / "world_continuity_model_role_assignment_plan_v1.json")
    inp = _load(root / "world_continuity_input_contract_v1.json")
    out = _load(root / "world_continuity_output_contract_v1.json")
    quality = _load(root / "world_continuity_quality_acceptance_plan_v1.json")
    health = _load(root / "world_continuity_health_validation_whitebox_plan_v1.json")
    prov_rt = _load(root / "world_continuity_provider_runtime_boundary_plan_v1.json")
    fallback = _load(root / "world_continuity_fallback_replacement_plan_v1.json")
    self_check = _load(root / "world_continuity_module_internal_self_check_plan_v1.json")
    interaction = _load(root / "world_continuity_midplatform_interaction_check_plan_v1.json")
    binding = _load(root / "world_continuity_midplatform_governance_binding_v1.json")
    ii = _load(root / "world_continuity_information_integration_handoff_plan_v1.json")
    dc = _load(root / "world_continuity_decision_center_handoff_plan_v1.json")
    wm_boundary = _load(root / "world_continuity_worldmodel_admission_boundary_plan_v1.json")
    mem_boundary = _load(root / "world_continuity_memory_admission_boundary_plan_v1.json")
    layer_dep = _load(root / "world_continuity_layer_dependency_review_v1.json")
    boundary = _load(root / "world_continuity_non_runtime_boundary_matrix_v1.json")
    qual = _load(root / "world_continuity_module_qualification_check_v1.json")
    dryrun = _load(root / "world_continuity_module_model_profile_governance_binding_dryrun_plan_v1.json")
    decision = _load(root / "world_continuity_module_model_profile_governance_binding_planning_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.module", summary.get("module_id") == MODULE_ID)
    ok("summary.layer2", summary.get("capability_layer") == "Layer 2 Spatiotemporal Continuity")
    ok("summary.refs4", summary.get("registry_model_profile_ref_count") == 4)
    ok("summary.qual_mode", summary.get("qualification_mode") == QUALIFICATION_MODE)
    ok("summary.qual_only", summary.get("qualification_check_only") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.registry", summary.get("registry_ref") == REGISTRY_REF)
    ok("summary.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("summary.no_wm", summary.get("worldmodel_write_now") is False)
    ok("summary.no_mem", summary.get("memory_write_now") is False)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.qual_only", policy.get("qualification_check_only") is True)
    ok("policy.layer2", "Layer 2 Spatiotemporal Continuity" in (policy.get("phase_goal") or ""))
    ok("policy.not_fact", "World Continuity candidate ≠ WorldModel fact" in (policy.get("phase_goal") or ""))
    ok("upstream.pass", upstream.get("review_pass") is True)

    ok(
        "gov_reuse.not_framework",
        gov_reuse.get("world_continuity_module_qualification_planning_not_new_framework") is True,
    )
    for std in REUSED_GOVERNANCE_STANDARDS:
        ok(f"gov_reuse.{std[:16]}", std in (gov_reuse.get("reused_standards") or []))

    ok("mod_def.id", mod_def.get("module_id") == MODULE_ID)
    ok("mod_def.layer2", mod_def.get("capability_layer") == "Layer 2 Spatiotemporal Continuity")
    ok("mod_def.l1", mod_def.get("supports_layer_1") == "Current Scene Understanding")
    ok("mod_def.l3", mod_def.get("supports_layer_3") == "Navigation Application")
    ok("mod_def.no_wm", mod_def.get("worldmodel_write_now") is False)
    ok("mod_def.no_mem", mod_def.get("memory_write_now") is False)
    ok("mod_def.candidate", mod_def.get("candidate_only") is True)
    mod_text = json.dumps(mod_def, ensure_ascii=False)
    ok("mod_def.not_fact", "World Continuity candidate ≠ WorldModel fact" in mod_text)

    stack_text = json.dumps(stack, ensure_ascii=False)
    ok("stack.l1", "visual_observation_candidate_ref" in stack_text)
    ok("stack.l2", "scene_delta_candidate" in stack_text)
    ok("stack.l3", "navigation_context_support_candidate" in stack_text)
    ok("stack.l4", "worldmodel_admission_candidate_later" in stack_text)
    ok("stack.no_wm", "no direct WorldModel write" in stack_text)

    gov_text = json.dumps(gov_map, ensure_ascii=False)
    ok("gov.l1", "cannot override raw evidence" in gov_text)
    ok("gov.l2_not_fact", "not_fact" in gov_text)
    ok("gov.l3_no_action", "cannot emit action" in gov_text)
    ok("gov.l4_admission", "WorldModel Admission required" in gov_text)

    ok("profile.id", profile.get("module_local_profile_id") == MODULE_LOCAL_PROFILE_ID)
    ok("profile.no_fact", profile.get("no_direct_fact_output") is True)
    ok("profile.no_wm", profile.get("no_direct_worldmodel_write") is True)
    ok("profile.no_mem", profile.get("no_direct_memory_write") is True)
    for ref in WORLD_CONTINUITY_REGISTRY_REFS:
        ok(f"profile.ref.{ref[:12]}", ref in (profile.get("registry_model_profile_refs") or []))

    ok("refs.pass", refs_review.get("review_pass") is True)
    ok("refs.stcm", STCM_REGISTRY_ID in json.dumps(refs_review))
    ok("refs.scene_delta", "scene_delta_candidate" in json.dumps(refs_review))

    roles_text = json.dumps(roles, ensure_ascii=False)
    ok("roles.scene_delta", "scene change candidate role" in roles_text)
    ok("roles.stcm", "governance-owned consistency manager role" in roles_text)
    ok("roles.no_truth", "no single model owns WorldModel truth" in roles_text)

    inp_text = json.dumps(inp, ensure_ascii=False)
    ok("inp.no_frames", "raw frame sequence not consumed now" in inp_text)
    ok("inp.no_tracking", "live tracking not executed now" in inp_text)

    out_text = json.dumps(out, ensure_ascii=False)
    ok("out.continuity", "world_continuity_candidate" in out_text)
    ok("out.scene_delta", "scene_delta_candidate" in out_text)
    for forbidden in IO_FORBIDDEN:
        ok(f"out.forbid.{forbidden[:14]}", forbidden in (out.get("forbidden_outputs") or []))

    ok("quality.benchmark_now", quality.get("benchmark_executed_now") is False)
    ok("quality.compliance", quality.get("candidate_contract_compliance_required") is True)

    ok("health.evidence_chain", health.get("evidence_chain_required") is True)
    ok("health.detail_false", health.get("health_metric_detail_defined_now") is False)
    ok("health.transport", health.get("health_status_ref_transport_only") is True)

    ok("prov.no_runtime", "World Continuity runtime remains disabled now" in json.dumps(prov_rt))

    ok("binding.id", binding.get("midplatform_governance_binding_id") == MIDPLATFORM_BINDING_ID)
    ok("binding.ii", bool(binding.get("information_integration_consumption_policy_ref")))
    ok("binding.wm_later", bool(binding.get("worldmodel_admission_requirement_ref_later")))
    ok("binding.mem_later", bool(binding.get("memory_admission_requirement_ref_later")))
    ok("binding.evidence", bool(binding.get("evidence_chain_requirement_ref")))
    ok("binding.constitution", binding.get("constitution_bus_ref") == CONSTITUTION_BUS_REF)
    ok("binding.no_runtime", binding.get("runtime_enabled_now") is False)

    ii_text = json.dumps(ii, ensure_ascii=False)
    ok("ii.no_bypass", "cannot bypass Information Integration to WorldModel write" in ii_text)

    dc_text = json.dumps(dc, ensure_ascii=False)
    ok("dc.no_decision", "cannot emit final decision" in dc_text)
    ok("dc.no_nav", "cannot directly trigger navigation action" in dc_text)

    wm_text = json.dumps(wm_boundary, ensure_ascii=False)
    ok("wm.no_write", "cannot write WorldModel" in wm_text)
    ok("wm.not_fact", "scene_delta candidate is not world fact" in wm_text)

    mem_text = json.dumps(mem_boundary, ensure_ascii=False)
    ok("mem.no_write", "cannot write Memory" in mem_text)

    layer_text = json.dumps(layer_dep, ensure_ascii=False)
    ok("layer.l1_dep", "depends on Layer 1 scene observations" in layer_text)
    ok("layer.no_override", "cannot override raw perception evidence" in layer_text)

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
    for item in WORLD_CONTINUITY_MIDPLATFORM_INTERACTION_CHECK_COVERAGE:
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
        "capability_layer": "Layer 2 Spatiotemporal Continuity",
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
