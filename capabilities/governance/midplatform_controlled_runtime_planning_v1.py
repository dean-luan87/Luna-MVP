# -*- coding: utf-8 -*-
"""Midplatform Controlled Runtime Planning v1 — planning only, no runtime execution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.health_enforcement_supervisor_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HEALTH_SUPERVISOR_DR_FINAL_GO,
    NEXT_PHASE_GO as HEALTH_SUPERVISOR_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL_GO,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FMIS_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-Controlled-Runtime-Planning-v1-001"
SCOPE = "controlled_runtime_planning_only"
SOURCE_CHAIN = "midplatform_controlled_runtime_planning_v1"

UPSTREAM_HEALTH_SUPERVISOR_DR_FINAL = HEALTH_SUPERVISOR_DR_FINAL_GO
UPSTREAM_HEALTH_SUPERVISOR_DR_NEXT = HEALTH_SUPERVISOR_DR_NEXT_PHASE

FINAL_DECISION_GO = "MIDPLATFORM_CONTROLLED_RUNTIME_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "MIDPLATFORM_CONTROLLED_RUNTIME_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Controlled-Runtime-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Controlled-Runtime-Issue-Review-v1-001"

CORE_CHAIN_BOUNDARY = (
    "controlled_runtime_candidate ≠ runtime enabled ≠ provider invoked ≠ execution authorized"
)

SCOPE_DEFINITION_RULES: Tuple[str, ...] = (
    "controlled runtime is a later runtime admission framework",
    "controlled runtime is not direct execution",
    "controlled runtime covers provider/model/tool/output runtime controlled admission",
    "controlled runtime must be constrained by Constitution / Resolver / Enforcement / Validation / Health / Provider Abstraction / Whitebox",
    "planning phase cannot open execution window",
)

IN_SCOPE_RUNTIMES: Tuple[str, ...] = (
    "OCR provider runtime later",
    "Vision provider runtime later",
    "ASR provider runtime later",
    "TTS provider runtime later",
    "Map provider runtime later",
    "Display Output runtime later",
    "Notification Output runtime later",
    "Voice Output / Audio playback runtime later",
)

EXCLUDED_RUNTIMES: Tuple[str, ...] = (
    "Memory write runtime",
    "WorldModel fact write runtime",
    "autonomous action execution",
    "production runtime",
    "uncontrolled provider invocation",
)

RUNTIME_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "runtime_candidate_id",
    "runtime_domain",
    "runtime_type",
    "upstream_gate_refs",
    "provider_candidate_refs",
    "readiness_refs",
    "authorization_required",
    "execution_window_required",
    "evidence_capture_required",
    "rollback_required",
    "post_execution_review_required",
    "health_supervision_required",
    "whitebox_trace_required",
    "runtime_enabled_now",
    "execution_started_now",
)

ADMISSION_RULES: Tuple[str, ...] = (
    "upstream simulated GO",
    "relevant gate result pass",
    "provider abstraction alignment pass",
    "provider readiness pass later",
    "validation pass later",
    "health supervision pass later",
    "no unresolved high-risk issue",
    "authorization request generated later",
    "execution window opened later",
    "rollback plan ready later",
    "evidence capture plan ready later",
)

AUTHORIZATION_RULES: Tuple[str, ...] = (
    "planning GO ≠ authorization granted",
    "runtime authorization requires owner/operator or governance approval later",
    "authorization must specify runtime_domain / provider_candidate / scope / window / rollback / evidence",
    "authorization cannot be implied from simulation GO",
    "authorization cannot be implied from provider readiness",
    "authorization cannot be implied from health signal",
)

EXECUTION_WINDOW_RULES: Tuple[str, ...] = (
    "runtime_execution_window_opened_now=false",
    "execution window must be time/scope/sandbox bounded",
    "execution window must bind provider candidate",
    "execution window must bind evidence path",
    "execution window must bind rollback path",
    "execution window cannot include production runtime by default",
)

PROVIDER_READINESS_RULES: Tuple[str, ...] = (
    "provider_candidate readiness required before runtime",
    "readiness pass ≠ selected provider",
    "selected provider ≠ invoked provider",
    "provider invocation requires execution window",
    "provider failure does not auto-switch",
    "provider switch requires separate policy",
    "provider abstraction standard required",
)

GATE_PRECONDITION_RULES: Tuple[str, ...] = (
    "Safety Gate / Speech Gate / Display Gate / Authorization Gate / Validation Factory results required where applicable",
    "execution runtime cannot read raw constitution",
    "execution runtime cannot bypass enforcement layer",
    "gate result candidates must be traceable",
    "gate fail/hold/block prevents runtime path",
)

HEALTH_SUPERVISION_RULES: Tuple[str, ...] = (
    "Health Enforcement Supervisor result required before controlled runtime",
    "health signal can recommend hold/degrade/escalation",
    "health signal cannot authorize runtime",
    "supervisor cannot directly block output",
    "supervisor issue traces must be reviewed later",
)

EVIDENCE_CAPTURE_FIELDS: Tuple[str, ...] = (
    "runtime_request_ref",
    "authorization_ref",
    "execution_window_ref",
    "provider_candidate_ref",
    "provider_readiness_ref",
    "gate_result_refs",
    "health_supervision_ref",
    "input_contract_ref",
    "output_contract_ref",
    "runtime_result_ref",
    "boundary_audit_ref",
    "failure_route_ref",
    "rollback_ref",
    "post_execution_review_ref",
)

ROLLBACK_RULES: Tuple[str, ...] = (
    "runtime failure cannot auto-repair",
    "runtime failure cannot auto-install/download",
    "runtime failure cannot auto-switch provider",
    "runtime failure cannot write Memory / WorldModel",
    "rollback route required before execution",
    "rollback result auditable later",
)

POST_EXECUTION_REVIEW_RULES: Tuple[str, ...] = (
    "every controlled runtime execution needs post-execution review",
    "review checks boundary, output, provider status, evidence, health, issue trace",
    "review outcome may be GO / HOLD / BLOCK / NEEDS_REPAIR",
    "review GO ≠ production readiness",
)

POST_EXECUTION_REVIEW_OUTCOMES: Tuple[str, ...] = ("GO", "HOLD", "BLOCK", "NEEDS_REPAIR")

FAILURE_ROUTES: Tuple[Dict[str, str], ...] = (
    {"trigger": "provider_not_ready", "route": "hold"},
    {"trigger": "provider_failure", "route": "issue_trace + fallback candidate"},
    {"trigger": "gate_fail", "route": "block runtime"},
    {"trigger": "health_pressure_high", "route": "hold/degrade"},
    {"trigger": "evidence_missing", "route": "hold"},
    {"trigger": "boundary_violation", "route": "violation_report"},
    {"trigger": "output_contract_violation", "route": "block + review"},
    {"trigger": "unexpected_runtime_side_effect", "route": "emergency hold"},
)

DOMAIN_MATRIX: Tuple[Dict[str, Any], ...] = (
    {
        "domain_id": "ocr_controlled_runtime",
        "label": "OCR controlled runtime",
        "required_gates": ["safety_gate", "authorization_gate", "validation_factory"],
        "provider_readiness_required": True,
        "authorization_required": True,
        "execution_window_required": True,
        "evidence_required": True,
        "rollback_required": True,
        "post_review_required": True,
        "runtime_enabled_now": False,
    },
    {
        "domain_id": "vision_controlled_runtime",
        "label": "Vision controlled runtime",
        "required_gates": ["safety_gate", "authorization_gate", "validation_factory"],
        "provider_readiness_required": True,
        "authorization_required": True,
        "execution_window_required": True,
        "evidence_required": True,
        "rollback_required": True,
        "post_review_required": True,
        "runtime_enabled_now": False,
    },
    {
        "domain_id": "asr_controlled_runtime",
        "label": "ASR controlled runtime",
        "required_gates": ["safety_gate", "authorization_gate", "validation_factory"],
        "provider_readiness_required": True,
        "authorization_required": True,
        "execution_window_required": True,
        "evidence_required": True,
        "rollback_required": True,
        "post_review_required": True,
        "runtime_enabled_now": False,
    },
    {
        "domain_id": "tts_controlled_runtime",
        "label": "TTS controlled runtime",
        "required_gates": [
            "safety_gate",
            "speech_gate",
            "authorization_gate",
            "validation_factory",
        ],
        "provider_readiness_required": True,
        "authorization_required": True,
        "execution_window_required": True,
        "evidence_required": True,
        "rollback_required": True,
        "post_review_required": True,
        "runtime_enabled_now": False,
    },
    {
        "domain_id": "map_controlled_runtime",
        "label": "Map controlled runtime",
        "required_gates": ["safety_gate", "authorization_gate", "validation_factory"],
        "provider_readiness_required": True,
        "authorization_required": True,
        "execution_window_required": True,
        "evidence_required": True,
        "rollback_required": True,
        "post_review_required": True,
        "runtime_enabled_now": False,
    },
    {
        "domain_id": "display_output_controlled_runtime",
        "label": "Display Output controlled runtime",
        "required_gates": [
            "safety_gate",
            "display_gate",
            "authorization_gate",
            "validation_factory",
        ],
        "provider_readiness_required": False,
        "authorization_required": True,
        "execution_window_required": True,
        "evidence_required": True,
        "rollback_required": True,
        "post_review_required": True,
        "runtime_enabled_now": False,
    },
    {
        "domain_id": "notification_output_controlled_runtime",
        "label": "Notification Output controlled runtime",
        "required_gates": [
            "safety_gate",
            "display_gate",
            "authorization_gate",
            "validation_factory",
        ],
        "provider_readiness_required": False,
        "authorization_required": True,
        "execution_window_required": True,
        "evidence_required": True,
        "rollback_required": True,
        "post_review_required": True,
        "runtime_enabled_now": False,
    },
    {
        "domain_id": "voice_output_audio_playback_controlled_runtime",
        "label": "Voice Output / Audio Playback controlled runtime",
        "required_gates": [
            "safety_gate",
            "speech_gate",
            "authorization_gate",
            "validation_factory",
        ],
        "provider_readiness_required": True,
        "authorization_required": True,
        "execution_window_required": True,
        "evidence_required": True,
        "rollback_required": True,
        "post_review_required": True,
        "runtime_enabled_now": False,
    },
)

RUNTIME_CANDIDATE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "runtime_candidate_id": "ocr_provider_runtime_candidate_v1",
        "runtime_domain": "OCR",
        "runtime_type": "provider_runtime",
        "provider_candidate_refs": ["paddleocr_candidate", "rapidocr_candidate"],
    },
    {
        "runtime_candidate_id": "vision_provider_runtime_candidate_v1",
        "runtime_domain": "Vision",
        "runtime_type": "provider_runtime",
        "provider_candidate_refs": ["vision_provider_candidate"],
    },
    {
        "runtime_candidate_id": "asr_provider_runtime_candidate_v1",
        "runtime_domain": "ASR",
        "runtime_type": "provider_runtime",
        "provider_candidate_refs": ["asr_provider_candidate"],
    },
    {
        "runtime_candidate_id": "tts_provider_runtime_candidate_v1",
        "runtime_domain": "TTS",
        "runtime_type": "provider_runtime",
        "provider_candidate_refs": [CURRENT_PREFERRED_PROVIDER_CANDIDATE],
    },
    {
        "runtime_candidate_id": "map_provider_runtime_candidate_v1",
        "runtime_domain": "Map",
        "runtime_type": "provider_runtime",
        "provider_candidate_refs": ["map_provider_candidate"],
    },
    {
        "runtime_candidate_id": "display_output_runtime_candidate_v1",
        "runtime_domain": "Display Output",
        "runtime_type": "output_runtime",
        "provider_candidate_refs": [],
    },
    {
        "runtime_candidate_id": "notification_output_runtime_candidate_v1",
        "runtime_domain": "Notification Output",
        "runtime_type": "output_runtime",
        "provider_candidate_refs": [],
    },
    {
        "runtime_candidate_id": "voice_output_audio_playback_runtime_candidate_v1",
        "runtime_domain": "Voice Output / Audio Playback",
        "runtime_type": "output_runtime",
        "provider_candidate_refs": [],
    },
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "controlled_runtime_enabled_now",
    "controlled_runtime_execution_started_now",
    "runtime_execution_window_opened_now",
    "provider_selected_now",
    "provider_invoked_now",
    "provider_imported_now",
    "model_runtime_invoked_now",
    "qianwen_tts_invoked_now",
    "paddleocr_invoked_now",
    "rapidocr_invoked_now",
    "vision_runtime_invoked_now",
    "ocr_runtime_invoked_now",
    "asr_runtime_invoked_now",
    "tts_runtime_invoked_now",
    "map_provider_invoked_now",
    "display_output_invoked_now",
    "notification_sent_now",
    "audio_synthesis_invoked_now",
    "audio_output_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Controlled Runtime Planning GO ≠ runtime enabled",
    "controlled runtime candidate ≠ execution authorized",
    "provider readiness policy ≠ provider selected",
    "execution window policy ≠ window opened",
    "next DryRunAndReview ≠ real runtime execution",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("controlled_runtime_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = BOUNDARY_MATRIX_FALSE

UPSTREAM_RUNTIME_LEAKAGE_FIELDS: Tuple[str, ...] = (
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "tts_runtime_invoked_now",
    "tts_invoked_now",
    "qianwen_tts_invoked_now",
    "display_output_invoked_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_controlled_runtime_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
        "core_chain_boundary": CORE_CHAIN_BOUNDARY,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _gate_refs_for_domain(domain_id: str) -> List[str]:
    for entry in DOMAIN_MATRIX:
        if entry.get("domain_id") == domain_id:
            return list(entry.get("required_gates") or [])
    return []


def _runtime_candidate(spec: Dict[str, Any], domain_id: str) -> Dict[str, Any]:
    return {
        "runtime_candidate_id": spec["runtime_candidate_id"],
        "runtime_domain": spec["runtime_domain"],
        "runtime_type": spec["runtime_type"],
        "upstream_gate_refs": _gate_refs_for_domain(domain_id),
        "provider_candidate_refs": list(spec.get("provider_candidate_refs") or []),
        "readiness_refs": [f"readiness:{spec['runtime_candidate_id']}"],
        "authorization_required": True,
        "execution_window_required": True,
        "evidence_capture_required": True,
        "rollback_required": True,
        "post_execution_review_required": True,
        "health_supervision_required": True,
        "whitebox_trace_required": True,
        "runtime_enabled_now": False,
        "execution_started_now": False,
    }


def _check_upstream_no_runtime_leakage(summary: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in UPSTREAM_RUNTIME_LEAKAGE_FIELDS:
        if field in summary and summary.get(field) is not False:
            issues.append(f"{field} must be false in upstream")
    return issues


def run_midplatform_controlled_runtime_planning_v1(
    *,
    health_enforcement_supervisor_dryrun_and_review_root: str,
    midplatform_display_gate_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_frontend_model_influence_simulation_dryrun_and_review_root: str,
    midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root: str,
    midplatform_tts_runtime_dryrun_and_review_root: str,
    midplatform_voice_output_plane_dryrun_and_review_root: str,
    midplatform_speech_gate_dryrun_and_review_root: str,
    midplatform_safety_gate_dryrun_and_review_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    health_dr_root = Path(health_enforcement_supervisor_dryrun_and_review_root).expanduser().resolve()
    display_dr_root = Path(midplatform_display_gate_dryrun_and_review_root).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    fmis_dr_root = Path(
        midplatform_frontend_model_influence_simulation_dryrun_and_review_root
    ).expanduser().resolve()
    e2e_dr_root = Path(
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root
    ).expanduser().resolve()
    tts_dr_root = Path(midplatform_tts_runtime_dryrun_and_review_root).expanduser().resolve()
    voice_dr_root = Path(midplatform_voice_output_plane_dryrun_and_review_root).expanduser().resolve()
    speech_dr_root = Path(midplatform_speech_gate_dryrun_and_review_root).expanduser().resolve()
    safety_dr_root = Path(midplatform_safety_gate_dryrun_and_review_root).expanduser().resolve()
    validation_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()

    health_dr_sm = _try_read_json(health_dr_root / "summary.json") or {}
    health_dr_vr = _try_read_json(health_dr_root / "verifier_report.json") or {}
    display_dr_vr = _try_read_json(display_dr_root / "verifier_report.json") or {}
    provider_dr_sm = _try_read_json(provider_dr_root / "summary.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    fmis_dr_sm = _try_read_json(fmis_dr_root / "summary.json") or {}
    fmis_dr_vr = _try_read_json(fmis_dr_root / "verifier_report.json") or {}
    e2e_dr_sm = _try_read_json(e2e_dr_root / "summary.json") or {}
    e2e_dr_vr = _try_read_json(e2e_dr_root / "verifier_report.json") or {}
    tts_dr_vr = _try_read_json(tts_dr_root / "verifier_report.json") or {}
    voice_dr_vr = _try_read_json(voice_dr_root / "verifier_report.json") or {}
    speech_dr_vr = _try_read_json(speech_dr_root / "verifier_report.json") or {}
    safety_dr_vr = _try_read_json(safety_dr_root / "verifier_report.json") or {}
    validation_dr_vr = _try_read_json(validation_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_health_supervisor_dryrun_root": str(health_dr_root),
        "upstream_display_gate_dryrun_root": str(display_dr_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_fmis_dryrun_root": str(fmis_dr_root),
        "upstream_e2e_simulation_dryrun_root": str(e2e_dr_root),
        "upstream_tts_runtime_dryrun_root": str(tts_dr_root),
        "upstream_voice_output_plane_dryrun_root": str(voice_dr_root),
        "upstream_speech_gate_dryrun_root": str(speech_dr_root),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_validation_engineering_separation_dryrun_root": str(validation_dr_root),
        "output_root": str(out_root),
    }

    if health_dr_vr.get("verifier") != "GO":
        blockers.append("Health Enforcement Supervisor DryRunAndReview verifier must be GO")
    if health_dr_sm.get("final_decision") != UPSTREAM_HEALTH_SUPERVISOR_DR_FINAL:
        blockers.append("health supervisor dryrun final_decision mismatch")
    if health_dr_sm.get("recommended_next_phase") != UPSTREAM_HEALTH_SUPERVISOR_DR_NEXT:
        blockers.append("health supervisor dryrun recommended_next_phase mismatch")
    if display_dr_vr.get("verifier") != "GO":
        blockers.append("Display Gate DryRunAndReview must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview must be GO")
    if provider_dr_sm.get("final_decision") != PROVIDER_ABS_DR_FINAL_GO:
        blockers.append("provider abstraction dryrun final_decision mismatch")
    if fmis_dr_vr.get("verifier") != "GO":
        blockers.append("Frontend Model Influence Simulation DryRunAndReview must be GO")
    if fmis_dr_sm.get("final_decision") != FMIS_DR_FINAL_GO:
        blockers.append("FMIS dryrun final_decision mismatch")
    if e2e_dr_vr.get("verifier") != "GO":
        blockers.append("E2E Output Chain Simulation DryRunAndReview must be GO")
    if e2e_dr_sm.get("final_decision") != E2E_DR_FINAL_GO:
        blockers.append("E2E simulation dryrun final_decision mismatch")
    if tts_dr_vr.get("verifier") != "GO":
        blockers.append("TTS Runtime DryRunAndReview must be GO")
    if voice_dr_vr.get("verifier") != "GO":
        blockers.append("Voice Output Plane DryRunAndReview must be GO")
    if speech_dr_vr.get("verifier") != "GO":
        blockers.append("Speech Gate DryRunAndReview must be GO")
    if safety_dr_vr.get("verifier") != "GO":
        blockers.append("Safety Gate DryRunAndReview must be GO")
    if validation_dr_vr.get("verifier") != "GO":
        blockers.append("Validation Engineering Separation DryRunAndReview must be GO")

    leakage_issues: List[str] = []
    for label, sm in (
        ("health_supervisor", health_dr_sm),
        ("display_gate", _try_read_json(display_dr_root / "summary.json") or {}),
        ("provider_abstraction", provider_dr_sm),
        ("fmis", fmis_dr_sm),
        ("e2e", e2e_dr_sm),
        ("tts", _try_read_json(tts_dr_root / "summary.json") or {}),
        ("voice", _try_read_json(voice_dr_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    upstream_readiness = {
        "review_id": "upstream_system_readiness_review_v1",
        "health_supervisor_dryrun_verifier": health_dr_vr.get("verifier"),
        "health_supervisor_final_decision": health_dr_sm.get("final_decision"),
        "display_gate_dryrun_verifier": display_dr_vr.get("verifier"),
        "provider_abstraction_dryrun_verifier": provider_dr_vr.get("verifier"),
        "fmis_dryrun_verifier": fmis_dr_vr.get("verifier"),
        "e2e_simulation_dryrun_verifier": e2e_dr_vr.get("verifier"),
        "system_level_simulated_go": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "planning_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    scope_definition = {
        "definition_id": "controlled_runtime_scope_definition_v1",
        "rules": list(SCOPE_DEFINITION_RULES),
        "in_scope_runtimes": list(IN_SCOPE_RUNTIMES),
        "excluded_runtimes": list(EXCLUDED_RUNTIMES),
        "rule_count": len(SCOPE_DEFINITION_RULES),
        **meta,
    }

    candidates = []
    for spec, domain in zip(RUNTIME_CANDIDATE_SPECS, DOMAIN_MATRIX):
        candidates.append({**_runtime_candidate(spec, domain["domain_id"]), **meta})

    candidate_registry = {
        "registry_id": "controlled_runtime_candidate_registry_v1",
        "candidates": candidates,
        "candidate_count": len(candidates),
        "all_runtime_enabled_now_false": all(c.get("runtime_enabled_now") is False for c in candidates),
        **meta,
    }

    admission_policy = {
        "policy_id": "controlled_runtime_admission_policy_v1",
        "rules": list(ADMISSION_RULES),
        "rule_count": len(ADMISSION_RULES),
        "planning_not_admission_granted": True,
        **meta,
    }

    authorization_policy = {
        "policy_id": "controlled_runtime_authorization_policy_v1",
        "rules": list(AUTHORIZATION_RULES),
        "rule_count": len(AUTHORIZATION_RULES),
        "authorization_granted_now": False,
        **meta,
    }

    execution_window_policy = {
        "policy_id": "controlled_runtime_execution_window_policy_v1",
        "rules": list(EXECUTION_WINDOW_RULES),
        "rule_count": len(EXECUTION_WINDOW_RULES),
        "runtime_execution_window_opened_now": False,
        **meta,
    }

    provider_readiness_policy = {
        "policy_id": "controlled_runtime_provider_readiness_policy_v1",
        "rules": list(PROVIDER_READINESS_RULES),
        "rule_count": len(PROVIDER_READINESS_RULES),
        "provider_abstraction_standard_required": True,
        **meta,
    }

    gate_precondition_policy = {
        "policy_id": "controlled_runtime_gate_precondition_policy_v1",
        "rules": list(GATE_PRECONDITION_RULES),
        "rule_count": len(GATE_PRECONDITION_RULES),
        **meta,
    }

    health_supervision_policy = {
        "policy_id": "controlled_runtime_health_supervision_policy_v1",
        "rules": list(HEALTH_SUPERVISION_RULES),
        "rule_count": len(HEALTH_SUPERVISION_RULES),
        "health_enforcement_supervisor_required": True,
        **meta,
    }

    evidence_capture_policy = {
        "policy_id": "controlled_runtime_evidence_capture_policy_v1",
        "required_fields": list(EVIDENCE_CAPTURE_FIELDS),
        "field_count": len(EVIDENCE_CAPTURE_FIELDS),
        "runtime_result_ref_later": True,
        **meta,
    }

    rollback_policy = {
        "policy_id": "controlled_runtime_rollback_policy_v1",
        "rules": list(ROLLBACK_RULES),
        "rule_count": len(ROLLBACK_RULES),
        **meta,
    }

    post_execution_review_policy = {
        "policy_id": "controlled_runtime_post_execution_review_policy_v1",
        "rules": list(POST_EXECUTION_REVIEW_RULES),
        "allowed_outcomes": list(POST_EXECUTION_REVIEW_OUTCOMES),
        "rule_count": len(POST_EXECUTION_REVIEW_RULES),
        **meta,
    }

    failure_route_policy = {
        "policy_id": "controlled_runtime_failure_route_policy_v1",
        "routes": list(FAILURE_ROUTES),
        "route_count": len(FAILURE_ROUTES),
        **meta,
    }

    domain_matrix = {
        "matrix_id": "controlled_runtime_domain_matrix_v1",
        "domains": list(DOMAIN_MATRIX),
        "domain_count": len(DOMAIN_MATRIX),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "controlled_runtime_boundary_matrix_v1",
        "all_runtime_actions_false": True,
        "matrix": {field: False for field in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "controlled_runtime_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate controlled_runtime_framework_candidate",
            "generate runtime_candidate_registry sample",
            "verify admission / authorization / window / provider readiness policies",
            "verify gate precondition / health supervision / evidence / rollback / post-review policies",
            "verify 8 domain controlled runtime matrix",
            "no real runtime enabled",
            "no provider invocation",
        ],
        **meta,
    }

    registry_ok = all(
        all(field in c for field in RUNTIME_CANDIDATE_FIELDS)
        and c.get("runtime_enabled_now") is False
        and c.get("execution_started_now") is False
        for c in candidates
    )
    domain_ok = all(d.get("runtime_enabled_now") is False for d in DOMAIN_MATRIX)
    planning_pass = input_ok and registry_ok and domain_ok

    planning_decision = {
        "decision_id": "controlled_runtime_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "main_chain_defined": [
            "simulated candidate chain (system-level GO)",
            "→ Controlled Runtime admission / authorization / execution window framework",
            "→ provider readiness + gate preconditions + health supervision",
            "→ evidence / rollback / post-review later",
            "→ controlled runtime execution later (not now)",
        ],
        **meta,
    }

    policy = {
        "policy_id": "controlled_runtime_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "controlled_runtime_not_execution": True,
        "planning_not_runtime_enable": True,
        "scope_definition_rules": list(SCOPE_DEFINITION_RULES),
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_pass,
        "violations": list(blockers),
        "planning_pass": planning_pass,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "controlled_runtime_planning_policy": policy,
        "upstream_system_readiness_review": upstream_readiness,
        "controlled_runtime_scope_definition": scope_definition,
        "controlled_runtime_candidate_registry": candidate_registry,
        "controlled_runtime_admission_policy": admission_policy,
        "controlled_runtime_authorization_policy": authorization_policy,
        "controlled_runtime_execution_window_policy": execution_window_policy,
        "controlled_runtime_provider_readiness_policy": provider_readiness_policy,
        "controlled_runtime_gate_precondition_policy": gate_precondition_policy,
        "controlled_runtime_health_supervision_policy": health_supervision_policy,
        "controlled_runtime_evidence_capture_policy": evidence_capture_policy,
        "controlled_runtime_rollback_policy": rollback_policy,
        "controlled_runtime_post_execution_review_policy": post_execution_review_policy,
        "controlled_runtime_failure_route_policy": failure_route_policy,
        "controlled_runtime_domain_matrix": domain_matrix,
        "controlled_runtime_boundary_matrix": boundary_matrix,
        "controlled_runtime_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "controlled_runtime_planning_decision": planning_decision,
        "summary": summary,
    }
