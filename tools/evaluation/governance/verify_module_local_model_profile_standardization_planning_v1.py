#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Module-local Model Profile Standardization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.model_profile_registry_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as REGISTRY_DR_FINAL_GO,
)
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    DOMAIN_COVERAGE,
    FINAL_DECISION_GO,
    IO_FORBIDDEN,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
    MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    DUAL_VALIDATION_MECHANISM_ID,
    DUAL_VALIDATION_NON_CLAIMS,
    MODULE_LOCAL_PROFILE_SCHEMA_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REGISTRY_REF,
    REUSED_GOVERNANCE_STANDARDS,
    SCOPE,
    STANDARD_DUTIES,
    STANDARD_NOT,
)

MIN_CHECKS = 246

REQUIRED = (
    "module_local_model_profile_standardization_planning_policy_v1.json",
    "model_profile_registry_input_review_v1.json",
    "governance_standard_reuse_review_v1.json",
    "module_local_model_profile_standard_definition_v1.json",
    "module_local_model_profile_schema_v1.json",
    "module_local_profile_to_registry_reference_policy_v1.json",
    "module_local_profile_capability_stack_binding_policy_v1.json",
    "module_local_profile_layered_governance_binding_policy_v1.json",
    "module_local_profile_input_output_binding_policy_v1.json",
    "module_local_profile_quality_acceptance_binding_policy_v1.json",
    "module_local_profile_health_validation_whitebox_binding_policy_v1.json",
    "module_local_profile_provider_runtime_boundary_policy_v1.json",
    "module_local_profile_fallback_replacement_policy_v1.json",
    "module_local_profile_midplatform_handoff_policy_v1.json",
    "module_internal_self_check_policy_v1.json",
    "midplatform_interaction_check_policy_v1.json",
    "vision_module_local_model_profile_template_v1.json",
    "ocr_module_local_model_profile_template_v1.json",
    "tts_module_local_model_profile_template_v1.json",
    "asr_module_local_model_profile_template_v1.json",
    "map_navigation_module_local_model_profile_template_v1.json",
    "world_continuity_module_local_model_profile_template_v1.json",
    "memory_emotion_evolution_module_local_model_profile_template_v1.json",
    "module_local_profile_domain_coverage_matrix_v1.json",
    "module_local_profile_non_runtime_boundary_matrix_v1.json",
    "module_local_profile_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "module_local_model_profile_standardization_planning_decision_v1.json",
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
            "module_local_model_profile_standardization_planning"
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

    registry_vr = _load(Path(args.registry_dryrun_root) / "verifier_report.json")
    registry_sm = _load(Path(args.registry_dryrun_root) / "summary.json")

    ok("upstream.registry_go", registry_vr.get("verifier") == "GO")
    ok("upstream.registry_final", registry_sm.get("final_decision") == REGISTRY_DR_FINAL_GO)

    summary = _load(root / "summary.json")
    policy = _load(root / "module_local_model_profile_standardization_planning_policy_v1.json")
    registry_in = _load(root / "model_profile_registry_input_review_v1.json")
    gov_reuse = _load(root / "governance_standard_reuse_review_v1.json")
    std_def = _load(root / "module_local_model_profile_standard_definition_v1.json")
    schema = _load(root / "module_local_model_profile_schema_v1.json")
    vision = _load(root / "vision_module_local_model_profile_template_v1.json")
    ocr = _load(root / "ocr_module_local_model_profile_template_v1.json")
    tts = _load(root / "tts_module_local_model_profile_template_v1.json")
    asr = _load(root / "asr_module_local_model_profile_template_v1.json")
    nav = _load(root / "map_navigation_module_local_model_profile_template_v1.json")
    world = _load(root / "world_continuity_module_local_model_profile_template_v1.json")
    mem = _load(root / "memory_emotion_evolution_module_local_model_profile_template_v1.json")
    domain_mx = _load(root / "module_local_profile_domain_coverage_matrix_v1.json")
    boundary = _load(root / "module_local_profile_non_runtime_boundary_matrix_v1.json")
    dryrun = _load(root / "module_local_profile_dryrun_plan_v1.json")
    decision = _load(root / "module_local_model_profile_standardization_planning_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.templates7", summary.get("template_count") == 7)
    ok("summary.domains10", summary.get("domain_coverage_count") == 10)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.registry", summary.get("registry_ref") == REGISTRY_REF)
    ok("summary.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("summary.reuse", summary.get("phase_governance_standard_reuse_rule") is True)
    ok("summary.new_false", summary.get("new_governance_need_proven") is False)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("summary.dual_val", summary.get("dual_validation_mechanism_ref") == DUAL_VALIDATION_MECHANISM_ID)
    ok("summary.dual_layers2", summary.get("dual_validation_layers") == 2)

    self_check = _load(root / "module_internal_self_check_policy_v1.json")
    interaction = _load(root / "midplatform_interaction_check_policy_v1.json")
    ok("self_check.layer", self_check.get("mechanism_layer") == "Module Internal Self-Check")
    ok("self_check.dual_ref", self_check.get("dual_validation_mechanism_ref") == DUAL_VALIDATION_MECHANISM_ID)
    ok("self_check.rules7", len(self_check.get("rules") or []) >= 7)
    for item in MODULE_INTERNAL_SELF_CHECK_COVERAGE:
        ok(f"self_check.{item[:16]}", item in (self_check.get("self_check_coverage") or []))
    ok("self_check.no_runtime", "自检不授权 runtime" in str(self_check.get("rules")))
    ok("self_check.no_select", "自检不选择模型" in str(self_check.get("rules")))
    ok("self_check.not_replace", self_check.get("does_not_replace") == "Midplatform Interaction Check")

    ok("interaction.layer", interaction.get("mechanism_layer") == "Midplatform Interaction Check")
    ok("interaction.dual_ref", interaction.get("dual_validation_mechanism_ref") == DUAL_VALIDATION_MECHANISM_ID)
    ok("interaction.rules5", len(interaction.get("rules") or []) >= 5)
    for item in MIDPLATFORM_INTERACTION_CHECK_COVERAGE:
        ok(f"interaction.{item[:16]}", item in (interaction.get("interaction_check_coverage") or []))
    ok("interaction.not_runtime", "不等于 runtime 授权" in str(interaction.get("rules")))
    ok("interaction.not_replace", interaction.get("does_not_replace") == "Module Internal Self-Check")

    ok("std_def.dual", std_def.get("dual_validation_mechanism", {}).get("mechanism_id") == DUAL_VALIDATION_MECHANISM_ID)

    for claim in DUAL_VALIDATION_NON_CLAIMS:
        ok(f"dual_claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("dual_validation_non_claims") or []))

    ok("policy.plan_only", policy.get("standardization_planning_only") is True)
    ok("registry_in.pass", registry_in.get("review_pass") is True)
    ok("registry_in.registry", registry_in.get("registry_id") == REGISTRY_REF)

    ok("gov_reuse.ref", gov_reuse.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("gov_reuse.rule", gov_reuse.get("phase_governance_standard_reuse_rule") is True)
    ok("gov_reuse.new_false", gov_reuse.get("new_governance_need_proven") is False)
    ok("gov_reuse.not_framework", gov_reuse.get("module_local_binding_standardization_not_new_framework") is True)
    for std in REUSED_GOVERNANCE_STANDARDS:
        ok(f"gov_reuse.{std[:16]}", std in (gov_reuse.get("reused_standards") or []))

    ok("std_def.id", std_def.get("standard_id") == "module_local_model_profile_standard_v1")
    ok("std_def.registry", std_def.get("registry_ref") == REGISTRY_REF)
    ok("std_def.no_runtime", std_def.get("module_local_profile_runtime_enabled_now") is False)
    ok("std_def.candidate", std_def.get("candidate_only") is True)
    for duty in STANDARD_DUTIES:
        ok(f"duty.{duty[:18]}", duty in (std_def.get("standard_duties") or []))
    for not_role in STANDARD_NOT:
        ok(f"not.{not_role[:18]}", not_role in (std_def.get("standard_is_not") or []))

    for field in MODULE_LOCAL_PROFILE_SCHEMA_FIELDS:
        ok(f"schema.{field[:16]}", field in (schema.get("required_fields") or []))
    ok("schema.no_override", schema.get("defaults", {}).get("no_registry_override") is True)
    ok("schema.no_select", schema.get("defaults", {}).get("no_model_selection_by_module") is True)
    ok("schema.no_invoke", schema.get("defaults", {}).get("no_model_invocation_by_profile") is True)

    reg_pol = _load(root / "module_local_profile_to_registry_reference_policy_v1.json")
    ok("reg_pol.rules6", len(reg_pol.get("rules") or []) >= 6)
    ok("reg_pol.registry", reg_pol.get("registry_ref") == REGISTRY_REF)

    stack_pol = _load(root / "module_local_profile_capability_stack_binding_policy_v1.json")
    ok("stack_pol.stack", stack_pol.get("capability_stack_ref") == STANDARD_ID)

    gov_pol = _load(root / "module_local_profile_layered_governance_binding_policy_v1.json")
    ok("gov_pol.addendum", gov_pol.get("layered_governance_mapping_ref") == ADDENDUM_ID)

    io_pol = _load(root / "module_local_profile_input_output_binding_policy_v1.json")
    for forbidden in IO_FORBIDDEN:
        ok(f"io.forbid.{forbidden[:14]}", forbidden in (io_pol.get("forbidden_outputs") or []))

    ok("qual_pol.rules", len(_load(root / "module_local_profile_quality_acceptance_binding_policy_v1.json").get("rules") or []) >= 6)
    ok("health_pol.rules", len(_load(root / "module_local_profile_health_validation_whitebox_binding_policy_v1.json").get("rules") or []) >= 6)
    ok("prov_pol.rules", len(_load(root / "module_local_profile_provider_runtime_boundary_policy_v1.json").get("rules") or []) >= 6)
    ok("fallback_pol.rules", len(_load(root / "module_local_profile_fallback_replacement_policy_v1.json").get("rules") or []) >= 5)
    ok("mid_pol.rules", len(_load(root / "module_local_profile_midplatform_handoff_policy_v1.json").get("rules") or []) >= 9)

    vision_text = json.dumps(vision, ensure_ascii=False)
    ok("vision.module", vision.get("module_id") == "vision_scene_understanding_module")
    ok("vision.yolo", "yolo_family" in vision_text)
    ok("vision.grounded", "grounded_sam" in vision_text)
    ok("vision.tracking", "visual_tracking" in vision_text)
    ok("vision.vlm", "vlm_scene" in vision_text)
    ok("vision.no_runtime", "no camera/runtime" in vision_text)
    ok("vision.no_fact", "no fact/action" in vision_text)

    ocr_text = json.dumps(ocr, ensure_ascii=False)
    ok("ocr.rapid", "rapidocr" in ocr_text)
    ok("ocr.paddle", "paddleocr" in ocr_text)
    ok("ocr.not_fact", "no fact" in ocr_text)
    ok("ocr.no_runtime", "no OCR runtime" in ocr_text)

    tts_text = json.dumps(tts, ensure_ascii=False)
    ok("tts.qianwen", "qianwen_tts" in tts_text)
    ok("tts.not_selected", "≠ selected" in tts_text)
    ok("tts.speech_gate", "Speech Gate" in tts_text)

    asr_text = json.dumps(asr, ensure_ascii=False)
    ok("asr.sensevoice", "sensevoice" in asr_text)
    ok("asr.no_runtime", "no ASR runtime" in asr_text)

    nav_text = json.dumps(nav, ensure_ascii=False)
    ok("nav.stage3", "Stage 3" in nav_text)
    ok("nav.no_invoke", "no map provider invocation" in nav_text)

    world_text = json.dumps(world, ensure_ascii=False)
    ok("world.stcm", "stcm_self_developed" in world_text)
    ok("world.signals", "signals only" in world_text)
    ok("world.no_wm", "no WorldModel write" in world_text)

    mem_text = json.dumps(mem, ensure_ascii=False)
    ok("mem.modules3", len(mem.get("modules") or []) == 3)
    ok("mem.proposal", "proposal_only" in mem_text)
    ok("mem.no_write", "no memory write" in mem_text)

    ok("domain.count10", domain_mx.get("domain_count") == len(DOMAIN_COVERAGE))
    ok("boundary.all_false", boundary.get("all_false") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:12]}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)
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
