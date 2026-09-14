#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Model Governance Binding Standardization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_BUS_DR_FINAL_GO,
)
from capabilities.governance.luna_gate_chain_enforcement_system_v1 import SYSTEM_ID as GATE_CHAIN_SYSTEM_ID
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONTROLLED_RUNTIME_DR_FINAL_GO,
)
from capabilities.governance.midplatform_display_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DISPLAY_GATE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_information_integration_layer_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as II_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SAFETY_GATE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_speech_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SPEECH_GATE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    BINDING_SCHEMA_FIELDS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CONSTITUTION_BUS_REF,
    CONTROLLED_RUNTIME_FRAMEWORK_REF,
    DOMAIN_COVERAGE,
    DUAL_VALIDATION_MECHANISM_ID,
    DUAL_VALIDATION_NON_CLAIMS,
    FINAL_DECISION_GO,
    INFORMATION_INTEGRATION_REF,
    LAYER_BINDING_SPECS,
    MODULE_LOCAL_PROFILE_STANDARD_REF,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PROVIDER_ABS_STANDARD_ID,
    REGISTRY_REF,
    REUSED_GOVERNANCE_STANDARDS,
    SCOPE,
    STANDARD_DUTIES,
    STANDARD_ID,
    STANDARD_NOT,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.model_profile_registry_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as REGISTRY_DR_FINAL_GO,
)
from capabilities.governance.module_local_model_profile_standardization_dryrun_and_review_v1 import (
    DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
    DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID,
    FINAL_DECISION_GO as MODULE_LOCAL_DR_FINAL_GO,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)

MIN_CHECKS = 306

REQUIRED = (
    "midplatform_model_governance_binding_standardization_planning_policy_v1.json",
    "module_local_profile_input_review_v1.json",
    "governance_standard_reuse_review_v1.json",
    "midplatform_model_governance_binding_standard_definition_v1.json",
    "midplatform_model_governance_binding_schema_v1.json",
    "constitution_bus_binding_policy_v1.json",
    "capability_bus_binding_policy_v1.json",
    "provider_abstraction_binding_policy_v1.json",
    "validation_binding_policy_v1.json",
    "health_oversight_binding_policy_v1.json",
    "whitebox_trace_binding_policy_v1.json",
    "information_integration_binding_policy_v1.json",
    "decision_center_binding_policy_v1.json",
    "gate_chain_binding_policy_v1.json",
    "controlled_runtime_binding_policy_v1.json",
    "memory_worldmodel_admission_binding_policy_v1.json",
    "model_governance_binding_by_capability_layer_v1.json",
    "model_governance_binding_by_module_domain_v1.json",
    "vision_model_governance_binding_template_v1.json",
    "ocr_model_governance_binding_template_v1.json",
    "tts_model_governance_binding_template_v1.json",
    "asr_model_governance_binding_template_v1.json",
    "map_navigation_model_governance_binding_template_v1.json",
    "world_continuity_model_governance_binding_template_v1.json",
    "memory_emotion_evolution_model_governance_binding_template_v1.json",
    "dual_validation_to_midplatform_binding_handoff_policy_v1.json",
    "non_compliance_handling_deferment_review_v1.json",
    "midplatform_model_governance_binding_non_runtime_boundary_matrix_v1.json",
    "midplatform_model_governance_binding_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "midplatform_model_governance_binding_standardization_planning_decision_v1.json",
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
            "midplatform_model_governance_binding_standardization_planning"
        ),
    )
    p.add_argument(
        "--module-local-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "module_local_model_profile_standardization_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--registry-dryrun-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_dryrun_and_review",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    ml_dr_vr = _load(Path(args.module_local_dryrun_root) / "verifier_report.json")
    ml_dr_sm = _load(Path(args.module_local_dryrun_root) / "summary.json")
    registry_vr = _load(Path(args.registry_dryrun_root) / "verifier_report.json")
    registry_sm = _load(Path(args.registry_dryrun_root) / "summary.json")

    ok("upstream.ml_dr_go", ml_dr_vr.get("verifier") == "GO")
    ok("upstream.ml_dr_final", ml_dr_sm.get("final_decision") == MODULE_LOCAL_DR_FINAL_GO)
    ok("upstream.ml_self_check", ml_dr_sm.get("module_internal_self_check_review_pass") is True)
    ok("upstream.ml_interaction", ml_dr_sm.get("midplatform_interaction_check_review_pass") is True)
    ok("upstream.registry_go", registry_vr.get("verifier") == "GO")
    ok("upstream.registry_final", registry_sm.get("final_decision") == REGISTRY_DR_FINAL_GO)

    summary = _load(root / "summary.json")
    policy = _load(
        root / "midplatform_model_governance_binding_standardization_planning_policy_v1.json"
    )
    ml_in = _load(root / "module_local_profile_input_review_v1.json")
    gov_reuse = _load(root / "governance_standard_reuse_review_v1.json")
    std_def = _load(root / "midplatform_model_governance_binding_standard_definition_v1.json")
    schema = _load(root / "midplatform_model_governance_binding_schema_v1.json")
    vision = _load(root / "vision_model_governance_binding_template_v1.json")
    ocr = _load(root / "ocr_model_governance_binding_template_v1.json")
    tts = _load(root / "tts_model_governance_binding_template_v1.json")
    asr = _load(root / "asr_model_governance_binding_template_v1.json")
    nav = _load(root / "map_navigation_model_governance_binding_template_v1.json")
    world = _load(root / "world_continuity_model_governance_binding_template_v1.json")
    mem = _load(root / "memory_emotion_evolution_model_governance_binding_template_v1.json")
    by_layer = _load(root / "model_governance_binding_by_capability_layer_v1.json")
    by_domain = _load(root / "model_governance_binding_by_module_domain_v1.json")
    boundary = _load(
        root / "midplatform_model_governance_binding_non_runtime_boundary_matrix_v1.json"
    )
    dryrun = _load(root / "midplatform_model_governance_binding_dryrun_plan_v1.json")
    deferment = _load(root / "non_compliance_handling_deferment_review_v1.json")
    decision = _load(
        root / "midplatform_model_governance_binding_standardization_planning_decision_v1.json"
    )
    dual_handoff = _load(root / "dual_validation_to_midplatform_binding_handoff_policy_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.templates7", summary.get("template_count") == 7)
    ok("summary.domains10", summary.get("domain_coverage_count") == 10)
    ok("summary.layers6", summary.get("layer_binding_count") == 6)
    ok("summary.policies11", summary.get("binding_policy_count") == 11)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.standard", summary.get("standard_id") == STANDARD_ID)
    ok("summary.registry", summary.get("registry_ref") == REGISTRY_REF)
    ok("summary.ml_std", summary.get("module_local_profile_standard_ref") == MODULE_LOCAL_PROFILE_STANDARD_REF)
    ok("summary.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("summary.reuse", summary.get("phase_governance_standard_reuse_rule") is True)
    ok("summary.new_false", summary.get("new_governance_need_proven") is False)
    ok("summary.deferred", summary.get("non_compliant_module_model_handling_policy_deferred") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.plan_only", policy.get("midplatform_model_governance_binding_standardization_planning_only") is True)

    ok("ml_in.pass", ml_in.get("review_pass") is True)
    ok("ml_in.self_check", ml_in.get("module_internal_self_check_review_pass") is True)
    ok("ml_in.interaction", ml_in.get("midplatform_interaction_check_review_pass") is True)
    ok("ml_in.ml_std", ml_in.get("module_local_profile_standard_ref") == MODULE_LOCAL_PROFILE_STANDARD_REF)

    ok("gov_reuse.ref", gov_reuse.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("gov_reuse.rule", gov_reuse.get("phase_governance_standard_reuse_rule") is True)
    ok("gov_reuse.new_false", gov_reuse.get("new_governance_need_proven") is False)
    ok("gov_reuse.not_framework", gov_reuse.get("midplatform_binding_standardization_not_new_framework") is True)
    for std in REUSED_GOVERNANCE_STANDARDS:
        ok(f"gov_reuse.{std[:16]}", std in (gov_reuse.get("reused_standards") or []))

    ok("std_def.id", std_def.get("standard_id") == STANDARD_ID)
    ok("std_def.type", std_def.get("standard_type") == "midplatform_model_profile_governance_binding_standard")
    ok("std_def.registry", std_def.get("registry_ref") == REGISTRY_REF)
    ok("std_def.ml_std", std_def.get("module_local_profile_standard_ref") == MODULE_LOCAL_PROFILE_STANDARD_REF)
    ok("std_def.dual", std_def.get("dual_validation_mechanism_ref") == DUAL_VALIDATION_MECHANISM_ID)
    ok("std_def.no_runtime", std_def.get("binding_runtime_enabled_now") is False)
    ok("std_def.no_select", std_def.get("model_selection_allowed_now") is False)
    ok("std_def.no_invoke", std_def.get("model_invocation_allowed_now") is False)
    ok("std_def.no_cr", std_def.get("controlled_runtime_allowed_now") is False)
    ok("std_def.candidate", std_def.get("candidate_only") is True)
    for duty in STANDARD_DUTIES:
        ok(f"duty.{duty[:18]}", duty in (std_def.get("standard_duties") or []))
    for not_role in STANDARD_NOT:
        ok(f"not.{not_role[:18]}", not_role in (std_def.get("standard_not") or []))

    for field in BINDING_SCHEMA_FIELDS:
        ok(f"schema.{field[:16]}", field in (schema.get("required_fields") or []))
    ok("schema.count30", schema.get("field_count") == len(BINDING_SCHEMA_FIELDS))
    ok("schema.no_select", schema.get("runtime_boundary_fields", {}).get("model_selected_now") is False)
    ok("schema.no_invoke", schema.get("runtime_boundary_fields", {}).get("model_invoked_now") is False)
    ok("schema.no_runtime", schema.get("runtime_boundary_fields", {}).get("runtime_enabled_now") is False)

    cb_pol = _load(root / "constitution_bus_binding_policy_v1.json")
    ok("cb.ref", cb_pol.get("constitution_bus_ref") == CONSTITUTION_BUS_REF)
    ok("cb.v1", cb_pol.get("constitution_bus_version") == "v1.0")
    cb_text = json.dumps(cb_pol, ensure_ascii=False)
    ok("cb.every_binding", "every midplatform binding must reference Constitution-Bus v1.0" in cb_text)
    ok("cb.no_raw", "raw constitution is not consumed directly" in cb_text)
    ok("cb.no_parallel", "module cannot create parallel governance" in cb_text)
    ok("cb.no_self_auth", "module cannot self-authorize" in cb_text)

    cap_pol = _load(root / "capability_bus_binding_policy_v1.json")
    cap_text = json.dumps(cap_pol, ensure_ascii=False)
    ok("cap.contract", "capability bus contract" in cap_text)
    ok("cap.no_invoke", "capability bus does not invoke model" in cap_text)
    ok("cap.blocks_admission", "missing capability bus contract blocks future module admission" in cap_text)

    prov_pol = _load(root / "provider_abstraction_binding_policy_v1.json")
    ok("prov.ref", prov_pol.get("provider_abstraction_ref") == PROVIDER_ABS_STANDARD_ID)
    prov_text = json.dumps(prov_pol, ensure_ascii=False)
    ok("prov.runtime_ne_provider", "runtime ≠ provider" in prov_text)
    ok("prov.candidate", "provider_candidate ≠ selected ≠ invoked" in prov_text)
    ok("prov.no_invoke_now", "cannot invoke provider now" in prov_text)

    val_pol = _load(root / "validation_binding_policy_v1.json")
    val_text = json.dumps(val_pol, ensure_ascii=False)
    ok("val.required", "validation_requirement_ref required" in val_text)
    ok("val.no_suppress", "validation failure cannot be suppressed" in val_text)
    ok("val.no_exec", "does not execute validation now" in val_text)

    health_pol = _load(root / "health_oversight_binding_policy_v1.json")
    health_text = json.dumps(health_pol, ensure_ascii=False)
    ok("health.required", "health_requirement_ref required" in health_text)
    ok("health.external", "Health Oversight remains external" in health_text)
    ok("health.transport", "Bus transports health_ref ≠ Bus judges health" in health_text)
    ok("health.no_self", "module cannot self-certify health" in health_text)
    ok("health.no_score", "does not generate health score now" in health_text)

    wb_pol = _load(root / "whitebox_trace_binding_policy_v1.json")
    wb_text = json.dumps(wb_pol, ensure_ascii=False)
    ok("wb.required", "whitebox_trace_requirement_ref required" in wb_text)
    ok("wb.explain", "explainable at candidate level" in wb_text)
    ok("wb.issue_trace", "issue_trace required" in wb_text)
    ok("wb.no_exec", "does not execute model" in wb_text)

    ii_pol = _load(root / "information_integration_binding_policy_v1.json")
    ok("ii.ref", ii_pol.get("information_integration_ref") == INFORMATION_INTEGRATION_REF)
    ii_text = json.dumps(ii_pol, ensure_ascii=False)
    ok("ii.flow", "Information Integration if context-relevant" in ii_text)
    ok("ii.candidate_only", "consumes candidate/context/signal only" in ii_text)
    ok("ii.no_bypass", "cannot bypass Information Integration to Decision Center" in ii_text)
    ok("ii.no_provider", "does not invoke provider" in ii_text)

    dc_pol = _load(root / "decision_center_binding_policy_v1.json")
    dc_text = json.dumps(dc_pol, ensure_ascii=False)
    ok("dc.integrated", "integrated_context / decision_request_candidate" in dc_text)
    ok("dc.no_direct", "model cannot emit decision directly" in dc_text)
    ok("dc.remains", "Decision Center remains" in dc_text)
    ok("dc.no_exec", "no decision executed now" in dc_text)

    gate_pol = _load(root / "gate_chain_binding_policy_v1.json")
    ok("gate.ref", gate_pol.get("gate_chain_system_ref") == GATE_CHAIN_SYSTEM_ID)
    gate_text = json.dumps(gate_pol, ensure_ascii=False)
    ok("gate.output_capable", "output-capable modules bind" in gate_text)
    ok("gate.candidate", "user_output_candidate ≠ user-facing output" in gate_text)
    ok("gate.result", "gate result candidate ≠ execution" in gate_text)
    ok("gate.privacy", "Privacy / Identity gates" in gate_text)

    cr_pol = _load(root / "controlled_runtime_binding_policy_v1.json")
    ok("cr.ref", cr_pol.get("controlled_runtime_framework_ref") == CONTROLLED_RUNTIME_FRAMEWORK_REF)
    cr_text = json.dumps(cr_pol, ensure_ascii=False)
    ok("cr.must_bind", "runtime-capable models must bind Controlled Runtime" in cr_text)
    ok("cr.no_enable", "binding does not enable runtime now" in cr_text)
    ok("cr.future", "controlled runtime readiness remains future phase" in cr_text)

    mem_pol = _load(root / "memory_worldmodel_admission_binding_policy_v1.json")
    mem_text = json.dumps(mem_pol, ensure_ascii=False)
    ok("mem.gate", "Memory Admission Gate later" in mem_text)
    ok("mem.wm_gate", "WorldModel Admission Gate later" in mem_text)
    ok("mem.no_direct", "cannot write Memory/WorldModel directly" in mem_text)
    ok("mem.personal", "Personal Continuity protections" in mem_text)

    ok("layer.count6", by_layer.get("layer_count") == len(LAYER_BINDING_SPECS))
    ok("layer.stack", by_layer.get("capability_stack_ref") == STACK_STANDARD_ID)
    ok("layer.addendum", by_layer.get("layered_governance_mapping_ref") == ADDENDUM_ID)
    layer_text = json.dumps(by_layer, ensure_ascii=False)
    ok("layer.l1_no_fact", "no direct fact/action" in layer_text)
    ok("layer.l2_no_wm", "no WorldModel write" in layer_text)
    ok("layer.l3_no_nav", "no direct navigation action" in layer_text)
    ok("layer.l4_no_identity", "no identity fact by default" in layer_text)
    ok("layer.l6_proposal", "proposal_only" in layer_text)
    ok("layer.l6_no_code", "no code modification" in layer_text)

    ok("domain.count10", by_domain.get("domain_count") == len(DOMAIN_COVERAGE))
    for d in DOMAIN_COVERAGE:
        ok(f"domain.{d[:12]}", any(x.get("domain") == d for x in (by_domain.get("domains") or [])))

    vision_text = json.dumps(vision, ensure_ascii=False)
    ok("vision.module", vision.get("module_id") == "vision_scene_understanding_module")
    ok("vision.yolo", "yolo_family" in vision_text)
    ok("vision.grounded", "grounded_sam" in vision_text)
    ok("vision.tracking", "visual_tracking" in vision_text)
    ok("vision.vlm", "vlm_scene" in vision_text)
    ok("vision.ii", "Information Integration" in vision_text)
    ok("vision.no_runtime", "no camera/runtime" in vision_text)
    ok("vision.no_fact", "no direct fact/action" in vision_text)
    ok("vision.bindings", len(vision.get("governance_bindings") or []) >= 4)

    ocr_text = json.dumps(ocr, ensure_ascii=False)
    ok("ocr.rapid", "rapidocr" in ocr_text)
    ok("ocr.paddle", "paddleocr" in ocr_text)
    ok("ocr.candidate", "candidate/evidence only" in ocr_text)
    ok("ocr.no_fact", "no fact/write/action" in ocr_text)

    tts_text = json.dumps(tts, ensure_ascii=False)
    ok("tts.qianwen", "qianwen_tts" in tts_text)
    ok("tts.not_selected", "≠ selected/invoked" in tts_text)
    ok("tts.speech_gate", "Speech Gate" in tts_text)
    ok("tts.no_audio", "no audio output now" in tts_text)

    asr_text = json.dumps(asr, ensure_ascii=False)
    ok("asr.sensevoice", "sensevoice" in asr_text)
    ok("asr.transcript", "transcript outputs candidate only" in asr_text)
    ok("asr.no_runtime", "no ASR runtime now" in asr_text)
    ok("asr.privacy", "Privacy/Identity gates" in asr_text)

    nav_text = json.dumps(nav, ensure_ascii=False)
    ok("nav.layer3", "navigation is Layer 3" in nav_text)
    ok("nav.no_invoke", "no map provider invocation" in nav_text)
    ok("nav.no_action", "no navigation action" in nav_text)

    world_text = json.dumps(world, ensure_ascii=False)
    ok("world.stcm", "stcm_self_developed" in world_text)
    ok("world.signals", "signals only" in world_text)
    ok("world.not_fact", "not WorldModel fact" in world_text)

    mem_tpl_text = json.dumps(mem, ensure_ascii=False)
    ok("mem.modules3", len(mem.get("modules") or []) == 3)
    ok("mem.personal", "Personal Continuity" in mem_tpl_text)
    ok("mem.proposal", "proposal_only" in mem_tpl_text)
    ok("mem.no_write", "no memory write" in mem_tpl_text)
    ok("mem.no_code", "no code modification" in mem_tpl_text)

    ok("dual.ref", dual_handoff.get("dual_validation_mechanism_ref") == DUAL_VALIDATION_MECHANISM_ID)
    dual_text = json.dumps(dual_handoff, ensure_ascii=False)
    ok("dual.self_check", "Module Internal Self-Check output" in dual_text)
    ok("dual.interaction", "Midplatform Interaction Check output" in dual_text)
    ok("dual.evidence", "evidence gates, not runtime gates" in dual_text)
    ok("dual.not_equal", "Self-Check GO ≠ Interaction Check GO" in dual_text)
    for claim in DUAL_VALIDATION_NON_CLAIMS:
        ok(f"dual_claim.{claim[:18]}", claim in (dual_handoff.get("dual_validation_non_claims") or []))

    ok("defer.deferred", deferment.get("non_compliant_module_model_handling_policy_deferred") is True)
    ok("defer.phase", deferment.get("recommended_future_phase") == DEFERRED_NON_COMPLIANCE_HANDLING_PHASE)
    ok("defer.policy", deferment.get("policy_ref_later") == DEFERRED_NON_COMPLIANCE_HANDLING_POLICY_ID)
    ok("defer.not_impl", deferment.get("not_implemented_now") is True)
    ok("defer.not_enforced", deferment.get("not_enforced_now") is True)
    ok("defer.ref_later", deferment.get("current_phase_may_reference_policy_ref_later_only") is True)
    defer_text = json.dumps(deferment, ensure_ascii=False)
    ok("defer.until_ml", "Module-local Model Profile Standardization DryRunAndReview completed" in defer_text)
    ok("defer.until_binding", "Midplatform Model Governance Binding Standardization completed later" in defer_text)

    ok("boundary.all_false", boundary.get("all_false") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:12]}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)
    dryrun_text = json.dumps(dryrun, ensure_ascii=False)
    ok("dryrun.schema", "verify binding schema" in dryrun_text)
    ok("dryrun.deferred", "non-compliance handling deferred" in dryrun_text)
    ok("dryrun.no_model", "no model select/download/invoke/benchmark" in dryrun_text)

    ok("decision.pass", decision.get("planning_pass") is True)
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
