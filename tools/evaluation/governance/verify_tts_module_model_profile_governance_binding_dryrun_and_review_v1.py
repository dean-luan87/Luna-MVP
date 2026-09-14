#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify TTS Module Model Profile + Governance Binding DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONSTITUTION_BUS_DR_FINAL_GO,
)
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONTROLLED_RUNTIME_DR_FINAL_GO,
)
from capabilities.governance.midplatform_model_governance_binding_standardization_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as BINDING_STD_DR_FINAL_GO,
)
from capabilities.governance.midplatform_speech_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SPEECH_GATE_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.model_profile_registry_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as REGISTRY_DR_FINAL_GO,
)
from capabilities.governance.module_local_model_profile_standardization_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as MODULE_LOCAL_DR_FINAL_GO,
)
from capabilities.governance.ocr_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as OCR_DR_FINAL_GO,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)
from capabilities.governance.tts_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CANDIDATE_REGISTRY_REFS,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
)
from capabilities.governance.tts_module_model_profile_governance_binding_planning_v1 import (
    CLOSURE_CAN_SAY,
    CLOSURE_CANNOT_SAY,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    IO_FORBIDDEN,
    MIDPLATFORM_BINDING_ID,
    MODULE_ID,
    MODULE_LOCAL_PROFILE_ID,
    QUALIFICATION_FIELDS,
    QUALIFICATION_MODE,
    SPEECH_GATE_REF,
    VOICE_OUTPUT_PLANE_REF,
)
from capabilities.governance.vision_module_model_profile_governance_binding_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VISION_DR_FINAL_GO,
)

MIN_CHECKS = 212

REQUIRED = (
    "tts_module_model_profile_governance_binding_dryrun_review_policy_v1.json",
    "planning_input_review_v1.json",
    "governance_standard_reuse_review_v1.json",
    "tts_module_model_profile_governance_binding_candidate_v1.json",
    "tts_module_definition_review_v1.json",
    "tts_capability_stack_review_v1.json",
    "tts_layered_governance_mapping_review_v1.json",
    "tts_module_local_model_profile_review_v1.json",
    "tts_model_profile_registry_refs_review_v1.json",
    "tts_model_role_assignment_review_v1.json",
    "tts_input_contract_review_v1.json",
    "tts_output_contract_review_v1.json",
    "tts_quality_acceptance_review_v1.json",
    "tts_health_validation_whitebox_review_v1.json",
    "tts_provider_runtime_boundary_review_v1.json",
    "tts_fallback_replacement_review_v1.json",
    "tts_module_internal_self_check_review_v1.json",
    "tts_midplatform_interaction_check_review_v1.json",
    "tts_midplatform_governance_binding_review_v1.json",
    "tts_speech_gate_handoff_review_v1.json",
    "tts_voice_output_plane_boundary_review_v1.json",
    "tts_memory_worldmodel_admission_boundary_review_v1.json",
    "tts_module_qualification_check_review_v1.json",
    "tts_non_runtime_boundary_audit_v1.json",
    "tts_blocked_path_result_v1.json",
    "tts_module_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)

REVIEW_FILES = (
    "governance_standard_reuse_review_v1.json",
    "tts_module_definition_review_v1.json",
    "tts_capability_stack_review_v1.json",
    "tts_layered_governance_mapping_review_v1.json",
    "tts_module_local_model_profile_review_v1.json",
    "tts_model_profile_registry_refs_review_v1.json",
    "tts_model_role_assignment_review_v1.json",
    "tts_input_contract_review_v1.json",
    "tts_output_contract_review_v1.json",
    "tts_quality_acceptance_review_v1.json",
    "tts_health_validation_whitebox_review_v1.json",
    "tts_provider_runtime_boundary_review_v1.json",
    "tts_fallback_replacement_review_v1.json",
    "tts_module_internal_self_check_review_v1.json",
    "tts_midplatform_interaction_check_review_v1.json",
    "tts_midplatform_governance_binding_review_v1.json",
    "tts_speech_gate_handoff_review_v1.json",
    "tts_voice_output_plane_boundary_review_v1.json",
    "tts_memory_worldmodel_admission_boundary_review_v1.json",
    "tts_module_qualification_check_review_v1.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _upstream_ok(root: Path, final_go: str) -> bool:
    vr = _load(root / "verifier_report.json")
    sm = _load(root / "summary.json")
    return vr.get("verifier") == "GO" and sm.get("final_decision") == final_go


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "tts_module_model_profile_governance_binding_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "tts_module_model_profile_governance_binding_planning"
        ),
    )
    p.add_argument("--ocr-dryrun-root", default=(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
        "ocr_module_model_profile_governance_binding_dryrun_and_review"
    ))
    p.add_argument("--vision-dryrun-root", default=(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
        "vision_module_model_profile_governance_binding_dryrun_and_review"
    ))
    p.add_argument("--binding-std-dryrun-root", default=(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
        "midplatform_model_governance_binding_standardization_dryrun_and_review"
    ))
    p.add_argument("--module-local-dryrun-root", default=(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
        "module_local_model_profile_standardization_dryrun_and_review"
    ))
    p.add_argument("--registry-dryrun-root", default=(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_dryrun_and_review"
    ))
    p.add_argument("--speech-gate-dryrun-root", default=(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review"
    ))
    p.add_argument("--constitution-dryrun-root", default=(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
        "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
    ))
    p.add_argument("--provider-abs-dryrun-root", default=(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
        "provider_abstraction_standard_alignment_dryrun_and_review"
    ))
    p.add_argument("--controlled-runtime-dryrun-root", default=(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
        "midplatform_controlled_runtime_dryrun_and_review"
    ))
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(Path(args.planning_root) / "verifier_report.json")
    plan_sm = _load(Path(args.planning_root) / "summary.json")
    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL_GO)
    ok("upstream.plan_module", plan_sm.get("module_id") == MODULE_ID)
    ok("upstream.plan_qual_only", plan_sm.get("qualification_check_only") is True)

    ok("upstream.ocr", _upstream_ok(Path(args.ocr_dryrun_root), OCR_DR_FINAL_GO))
    ok("upstream.vision", _upstream_ok(Path(args.vision_dryrun_root), VISION_DR_FINAL_GO))
    ok("upstream.binding_std", _upstream_ok(Path(args.binding_std_dryrun_root), BINDING_STD_DR_FINAL_GO))
    ok("upstream.module_local", _upstream_ok(Path(args.module_local_dryrun_root), MODULE_LOCAL_DR_FINAL_GO))
    ok("upstream.registry", _upstream_ok(Path(args.registry_dryrun_root), REGISTRY_DR_FINAL_GO))
    ok("upstream.speech_gate", _upstream_ok(Path(args.speech_gate_dryrun_root), SPEECH_GATE_DR_FINAL_GO))
    ok("upstream.constitution", _upstream_ok(Path(args.constitution_dryrun_root), CONSTITUTION_BUS_DR_FINAL_GO))
    ok("upstream.provider_abs", _upstream_ok(Path(args.provider_abs_dryrun_root), PROVIDER_ABS_DR_FINAL_GO))
    ok("upstream.controlled_runtime", _upstream_ok(
        Path(args.controlled_runtime_dryrun_root), CONTROLLED_RUNTIME_DR_FINAL_GO
    ))

    summary = _load(root / "summary.json")
    policy = _load(root / "tts_module_model_profile_governance_binding_dryrun_review_policy_v1.json")
    planning_input = _load(root / "planning_input_review_v1.json")
    candidate = _load(root / "tts_module_model_profile_governance_binding_candidate_v1.json")
    boundary = _load(root / "tts_non_runtime_boundary_audit_v1.json")
    blocked = _load(root / "tts_blocked_path_result_v1.json")
    closure = _load(root / "tts_module_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    qual_review = _load(root / "tts_module_qualification_check_review_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.module", summary.get("module_id") == MODULE_ID)
    ok("summary.qual_mode", summary.get("qualification_mode") == QUALIFICATION_MODE)
    ok("summary.qual_only", summary.get("qualification_check_only") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.qual_only", policy.get("qualification_check_only") is True)
    ok("planning_input.pass", planning_input.get("review_pass") is True)

    ok("candidate.id", candidate.get("candidate_id") == "tts_module_model_profile_governance_binding_candidate_v1")
    ok("candidate.module", candidate.get("module_id") == MODULE_ID)
    ok("candidate.profile", candidate.get("module_local_profile_ref") == MODULE_LOCAL_PROFILE_ID)
    ok("candidate.binding", candidate.get("midplatform_governance_binding_ref") == MIDPLATFORM_BINDING_ID)
    ok("candidate.qual_only", candidate.get("qualification_check_only") is True)
    ok("candidate.no_runtime", candidate.get("runtime_enabled_now") is False)
    ok("candidate.no_audio", candidate.get("audio_generated_now") is False)
    ok("candidate.no_vop", candidate.get("voice_output_plane_invoked_now") is False)
    ok("candidate.no_select", candidate.get("model_selected_now") is False)
    ok("candidate.no_invoke", candidate.get("model_invoked_now") is False)
    ok("candidate.qual_pass", candidate.get("qualification_pass") is True)
    for ref in CANDIDATE_REGISTRY_REFS:
        ok(f"candidate.ref.{ref[:14]}", ref in (candidate.get("registry_model_profile_refs") or []))

    for review_file in REVIEW_FILES:
        ok(f"review.{review_file[:28]}", _load(root / review_file).get("review_pass") is True)

    ok("boundary.audit_pass", boundary.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:20]}", (boundary.get("boundary_fields") or {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count", blocked.get("blocked_count") == len(BLOCKED_PATHS))
    for path_id in BLOCKED_PATHS:
        entries = blocked.get("blocked_paths") or []
        entry = next((e for e in entries if e.get("path_id") == path_id), {})
        ok(f"blocked.{path_id[:22]}", entry.get("status") == "blocked" and entry.get("executed") is False)

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    for item in CLOSURE_CAN_SAY:
        ok(f"closure.can.{item[:16]}", item in (closure.get("closure_can_say") or []))
    for item in CLOSURE_CANNOT_SAY:
        ok(f"closure.cannot.{item[:16]}", item in (closure.get("closure_cannot_say") or []))

    ok("next.asr", next_route.get("ready_for_asr_module_model_profile_governance_binding_planning") is True)
    ok("next.phase", next_route.get("selected_next_phase") == NEXT_PHASE_GO)

    ok("qual_review.pass", qual_review.get("review_pass") is True)
    for k, v in QUALIFICATION_FIELDS.items():
        ok(f"qual.{k[:18]}", qual_review.get(k) is v)

    binding_review = _load(root / "tts_midplatform_governance_binding_review_v1.json")
    ok("binding.speech_gate", any(
        c.get("check_id") == "speech_gate" and c.get("pass")
        for c in (binding_review.get("checks") or [])
    ))
    ok("binding.vop_later", any(
        c.get("check_id") == "vop_later" and c.get("pass")
        for c in (binding_review.get("checks") or [])
    ))

    out_review = _load(root / "tts_output_contract_review_v1.json")
    for forbidden in IO_FORBIDDEN:
        ok(f"out.forbid.{forbidden[:14]}", any(
            c.get("check_id") == f"forbid.{forbidden[:14]}" and c.get("pass")
            for c in (out_review.get("checks") or [])
        ))

    refs_review = _load(root / "tts_model_profile_registry_refs_review_v1.json")
    ok("refs.placeholder", any(
        c.get("check_id") == "placeholder" and c.get("pass")
        for c in (refs_review.get("checks") or [])
    ))

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
        "dryrun_and_review_pass": summary.get("dryrun_and_review_pass"),
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
