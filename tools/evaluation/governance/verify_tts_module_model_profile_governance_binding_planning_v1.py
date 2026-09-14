#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify TTS Module Model Profile + Governance Binding Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    CONSTITUTION_BUS_REF,
    CONTROLLED_RUNTIME_FRAMEWORK_REF,
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
from capabilities.governance.tts_module_model_profile_governance_binding_planning_v1 import (
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
    SPEECH_GATE_REF,
    TTS_MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    TTS_REGISTRY_REFS,
    VOICE_OUTPUT_PLANE_REF,
)
from capabilities.governance.vision_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VISION_DR_FINAL_GO,
)
from capabilities.governance.vision_module_model_profile_governance_binding_planning_v1 import (
    QUALIFICATION_CHECK_CRITERIA,
    QUALIFICATION_MODE,
)

MIN_CHECKS = 209

REQUIRED = (
    "tts_module_model_profile_governance_binding_planning_policy_v1.json",
    "upstream_ocr_module_input_review_v1.json",
    "governance_standard_reuse_review_v1.json",
    "tts_module_definition_v1.json",
    "tts_capability_stack_definition_v1.json",
    "tts_layered_governance_mapping_v1.json",
    "tts_module_local_model_profile_v1.json",
    "tts_model_profile_registry_refs_review_v1.json",
    "tts_model_role_assignment_plan_v1.json",
    "tts_input_contract_v1.json",
    "tts_output_contract_v1.json",
    "tts_quality_acceptance_plan_v1.json",
    "tts_health_validation_whitebox_plan_v1.json",
    "tts_provider_runtime_boundary_plan_v1.json",
    "tts_fallback_replacement_plan_v1.json",
    "tts_module_internal_self_check_plan_v1.json",
    "tts_midplatform_interaction_check_plan_v1.json",
    "tts_midplatform_governance_binding_v1.json",
    "tts_speech_gate_handoff_plan_v1.json",
    "tts_voice_output_plane_boundary_plan_v1.json",
    "tts_memory_worldmodel_admission_boundary_plan_v1.json",
    "tts_module_qualification_check_v1.json",
    "tts_non_runtime_boundary_matrix_v1.json",
    "tts_module_model_profile_governance_binding_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "tts_module_model_profile_governance_binding_planning_decision_v1.json",
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
            "tts_module_model_profile_governance_binding_planning"
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
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    ocr_dr_vr = _load(Path(args.ocr_dryrun_root) / "verifier_report.json")
    ocr_dr_sm = _load(Path(args.ocr_dryrun_root) / "summary.json")
    vision_dr_vr = _load(Path(args.vision_dryrun_root) / "verifier_report.json")
    vision_dr_sm = _load(Path(args.vision_dryrun_root) / "summary.json")
    ok("upstream.ocr_go", ocr_dr_vr.get("verifier") == "GO")
    ok("upstream.ocr_final", ocr_dr_sm.get("final_decision") == OCR_DR_FINAL_GO)
    ok("upstream.vision_go", vision_dr_vr.get("verifier") == "GO")
    ok("upstream.vision_final", vision_dr_sm.get("final_decision") == VISION_DR_FINAL_GO)

    summary = _load(root / "summary.json")
    policy = _load(root / "tts_module_model_profile_governance_binding_planning_policy_v1.json")
    upstream = _load(root / "upstream_ocr_module_input_review_v1.json")
    gov_reuse = _load(root / "governance_standard_reuse_review_v1.json")
    mod_def = _load(root / "tts_module_definition_v1.json")
    stack = _load(root / "tts_capability_stack_definition_v1.json")
    gov_map = _load(root / "tts_layered_governance_mapping_v1.json")
    profile = _load(root / "tts_module_local_model_profile_v1.json")
    refs_review = _load(root / "tts_model_profile_registry_refs_review_v1.json")
    roles = _load(root / "tts_model_role_assignment_plan_v1.json")
    inp = _load(root / "tts_input_contract_v1.json")
    out = _load(root / "tts_output_contract_v1.json")
    quality = _load(root / "tts_quality_acceptance_plan_v1.json")
    health = _load(root / "tts_health_validation_whitebox_plan_v1.json")
    prov_rt = _load(root / "tts_provider_runtime_boundary_plan_v1.json")
    fallback = _load(root / "tts_fallback_replacement_plan_v1.json")
    self_check = _load(root / "tts_module_internal_self_check_plan_v1.json")
    interaction = _load(root / "tts_midplatform_interaction_check_plan_v1.json")
    binding = _load(root / "tts_midplatform_governance_binding_v1.json")
    speech_gate = _load(root / "tts_speech_gate_handoff_plan_v1.json")
    vop = _load(root / "tts_voice_output_plane_boundary_plan_v1.json")
    mem_wm = _load(root / "tts_memory_worldmodel_admission_boundary_plan_v1.json")
    boundary = _load(root / "tts_non_runtime_boundary_matrix_v1.json")
    qual = _load(root / "tts_module_qualification_check_v1.json")
    dryrun = _load(root / "tts_module_model_profile_governance_binding_dryrun_plan_v1.json")
    decision = _load(root / "tts_module_model_profile_governance_binding_planning_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.module", summary.get("module_id") == MODULE_ID)
    ok("summary.refs3", summary.get("registry_model_profile_ref_count") == 3)
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
    ok("upstream.pass", upstream.get("review_pass") is True)

    ok("gov_reuse.not_framework", gov_reuse.get("tts_module_qualification_planning_not_new_framework") is True)
    for std in REUSED_GOVERNANCE_STANDARDS:
        ok(f"gov_reuse.{std[:16]}", std in (gov_reuse.get("reused_standards") or []))

    ok("mod_def.id", mod_def.get("module_id") == MODULE_ID)
    ok("mod_def.primary", mod_def.get("primary_goal") == "speech_synthesis_candidate_generation_later")
    ok("mod_def.no_runtime", mod_def.get("runtime_enabled_now") is False)
    ok("mod_def.no_audio", mod_def.get("audio_generated_now") is False)
    ok("mod_def.no_vop", mod_def.get("voice_output_plane_invoked_now") is False)
    ok("mod_def.candidate", mod_def.get("candidate_only") is True)
    mod_text = json.dumps(mod_def, ensure_ascii=False)
    ok("mod_def.no_speech_gate_bypass", "does not bypass Speech Gate" in mod_text)

    stack_text = json.dumps(stack, ensure_ascii=False)
    ok("stack.l1", "user_output_candidate_ref_later" in stack_text)
    ok("stack.l2", "tts_request_candidate_later" in stack_text)
    ok("stack.l3", "voice_output_plane_request_later" in stack_text)
    ok("stack.l4", "voice_persona_candidate_later" in stack_text)
    ok("stack.no_playback", "no direct audio playback" in stack_text)

    gov_text = json.dumps(gov_map, ensure_ascii=False)
    ok("gov.l1_gate", "speech_gate_required" in gov_text)
    ok("gov.l2_quality", "synthesis_quality_later" in gov_text)
    ok("gov.l3_vop", "Voice Output Plane required" in gov_text)
    ok("gov.no_audio_without", "no audio output without Speech Gate + Voice Output Plane" in gov_text)

    ok("profile.id", profile.get("module_local_profile_id") == MODULE_LOCAL_PROFILE_ID)
    ok("profile.health_later", profile.get("health_requirement_ref") == "required_later")
    ok("profile.no_user_out", profile.get("no_direct_user_output") is True)
    for ref in TTS_REGISTRY_REFS:
        ok(f"profile.ref.{ref[:12]}", ref in (profile.get("registry_model_profile_refs") or []))

    ok("refs.pass", refs_review.get("review_pass") is True)
    ok("refs.qianwen", "qianwen_tts_candidate" in json.dumps(refs_review))
    ok("refs.moss", "moss_tts_style_candidate" in json.dumps(refs_review))

    roles_text = json.dumps(roles, ensure_ascii=False)
    ok("roles.qianwen", "Qianwen TTS maps" in roles_text)
    ok("roles.moss", "MOSS TTS style maps" in roles_text)
    ok("roles.not_playback", "TTS candidate ≠ audio playback" in roles_text)

    inp_text = json.dumps(inp, ensure_ascii=False)
    ok("inp.no_raw", "raw user text cannot directly trigger TTS" in inp_text)
    ok("inp.speech_gate", "Speech Gate result required later" in inp_text)
    ok("inp.no_request", "no TTS request generated now" in inp_text)

    out_text = json.dumps(out, ensure_ascii=False)
    ok("out.audio_later", "audio_artifact_candidate_later" in out_text)
    for forbidden in IO_FORBIDDEN:
        ok(f"out.forbid.{forbidden[:14]}", forbidden in (out.get("forbidden_outputs") or []))

    ok("quality.benchmark_now", quality.get("benchmark_executed_now") is False)

    ok("health.health_later", health.get("health_requirement_ref") == "required_later")
    ok("health.detail_false", health.get("health_metric_detail_defined_now") is False)
    ok("health.no_self", health.get("module_cannot_self_certify_health") is True)

    ok("prov.no_runtime", "TTS runtime remains disabled now" in json.dumps(prov_rt))

    ok("binding.id", binding.get("midplatform_governance_binding_id") == MIDPLATFORM_BINDING_ID)
    ok("binding.speech_gate", binding.get("speech_gate_requirement_ref") == SPEECH_GATE_REF)
    ok("binding.vop_later", binding.get("voice_output_plane_requirement_ref_later") == VOICE_OUTPUT_PLANE_REF)
    ok("binding.constitution", binding.get("constitution_bus_ref") == CONSTITUTION_BUS_REF)
    ok("binding.cr", binding.get("controlled_runtime_requirement_ref") == CONTROLLED_RUNTIME_FRAMEWORK_REF)
    ok("binding.no_runtime", binding.get("runtime_enabled_now") is False)

    speech_text = json.dumps(speech_gate, ensure_ascii=False)
    ok("speech.no_before", "TTS does not run before Speech Gate" in speech_text)
    ok("speech.no_consume", "no speech_gate_result consumed now" in speech_text)

    vop_text = json.dumps(vop, ensure_ascii=False)
    ok("vop.not_playback", "TTS synthesis candidate ≠ playback" in vop_text)
    ok("vop.no_invoke", "no Voice Output Plane invoked now" in vop_text)

    mem_text = json.dumps(mem_wm, ensure_ascii=False)
    ok("mem.no_write", "cannot write Memory" in mem_text)

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

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    for item in MODULE_INTERNAL_SELF_CHECK_COVERAGE:
        ok(f"self_check.{item[:16]}", item in (self_check.get("self_check_coverage") or []))
    for item in TTS_MIDPLATFORM_INTERACTION_CHECK_COVERAGE:
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
