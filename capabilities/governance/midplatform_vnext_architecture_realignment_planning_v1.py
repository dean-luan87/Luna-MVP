# -*- coding: utf-8 -*-
"""Midplatform vNext Architecture Realignment Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CONTROLLED_RUNTIME_DR_FINAL_GO,
    NEXT_PHASE_GO as CONTROLLED_RUNTIME_DR_NEXT_PHASE,
)
from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL_GO,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FMIS_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL_GO,
)

PHASE_ID = "Phase-Midplatform-vNext-Architecture-Realignment-Planning-v1-001"
SCOPE = "architecture_realignment_planning_only"
SOURCE_CHAIN = "midplatform_vnext_architecture_realignment_planning_v1"

UPSTREAM_CONTROLLED_RUNTIME_DR_FINAL = CONTROLLED_RUNTIME_DR_FINAL_GO
UPSTREAM_CONTROLLED_RUNTIME_DR_NEXT = CONTROLLED_RUNTIME_DR_NEXT_PHASE

FINAL_DECISION_GO = (
    "MIDPLATFORM_VNEXT_ARCHITECTURE_REALIGNMENT_PLANNING_READY_FOR_COGNITIVE_ZONING_ARCHITECTURE_PLANNING"
)
FINAL_DECISION_HOLD = "MIDPLATFORM_VNEXT_ARCHITECTURE_REALIGNMENT_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Cognitive-Zoning-Architecture-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-vNext-Architecture-Realignment-Issue-Review-v1-001"

VNEXT_LAYERS: Tuple[Dict[str, str], ...] = (
    {
        "layer_id": "layer_0",
        "layer_index": "0",
        "layer_name": "Luna Seed Core",
        "role": "fixed life kernel; invariant across hardware/model/provider/version",
    },
    {
        "layer_id": "layer_1",
        "layer_index": "1",
        "layer_name": "Reusable Governance Standard Layer",
        "role": "reusable governance standards; modules must not build parallel governance",
    },
    {
        "layer_id": "layer_2",
        "layer_index": "2",
        "layer_name": "Cognitive Zoning Layer",
        "role": "cognitive zones; prevents universal brain",
    },
    {
        "layer_id": "layer_3",
        "layer_index": "3",
        "layer_name": "Information Integration / Decision Layer",
        "role": "information integration and decision; does not replace all zones",
    },
    {
        "layer_id": "layer_4",
        "layer_index": "4",
        "layer_name": "Pluggable Capability Layer",
        "role": "pluggable capabilities; varies with product form",
    },
    {
        "layer_id": "layer_5",
        "layer_index": "5",
        "layer_name": "Controlled Runtime Layer",
        "role": "later runtime admission framework; not execution now",
    },
    {
        "layer_id": "layer_6",
        "layer_index": "6",
        "layer_name": "Product Form Layer",
        "role": "product form variants; Badge/Glasses/Phone/Desktop/Home/Robot/Cloud",
    },
)

SEED_CORE_COMPONENTS: Tuple[str, ...] = (
    "Survival Drive",
    "Task Drive",
    "Resource Governance",
    "Health Management",
    "System Optimization",
    "Autonomous World Observation",
    "Seed Core Signal Bus",
)

SEED_CORE_CONFIRMATIONS: Tuple[str, ...] = (
    "Seed Core influences behavior but does not directly execute behavior",
    "Seed Core emits signals / hints / candidates, not facts/actions/user output",
    "Seed Core does not invoke provider",
    "Seed Core does not open runtime",
    "Seed Core does not write Memory / WorldModel",
    "Seed Core does not replace Decision Center",
    "Seed Core does not become universal brain",
)

GOVERNANCE_STANDARDS: Tuple[str, ...] = (
    "Module Definition Template",
    "Candidate / Evidence Contract",
    "Provider Abstraction Standard",
    "Validation Engineering Standard",
    "Gate / Enforcement Standard",
    "Controlled Runtime Standard",
    "Health Supervision Standard",
    "Whitebox Trace Standard",
    "Input / Output Boundary Standard",
    "Non-Claims Standard",
)

GOVERNANCE_STANDARD_CONFIRMATIONS: Tuple[str, ...] = (
    "future modules must reuse governance standards",
    "modules may provide domain_config but cannot create parallel governance systems",
    "no module sovereignty",
    "common governance before capability expansion",
)

COGNITIVE_ZONES: Tuple[str, ...] = (
    "Perception Zone",
    "Memory / WorldModel Zone",
    "Drive Zone",
    "Information Integration Zone",
    "Decision Zone",
    "Language / Output Zone",
    "Execution Zone",
    "Governance Zone",
)

COGNITIVE_ZONING_CONFIRMATIONS: Tuple[str, ...] = (
    "no single model owns perception + memory + drive + decision + output",
    "models produce candidates, not authority",
    "zones communicate through contracts/signals/candidates/evidence",
    "midplatform governs contracts, routing, boundary, supervision, not cognition itself",
)

PLUGGABLE_CAPABILITY_TYPES: Tuple[str, ...] = (
    "Vision / OCR / ASR / TTS / Map",
    "Memory / Library / Hive",
    "Display / Notification / Voice Output",
    "Provider adapters",
    "Hardware sensors",
    "Device-specific runtime",
    "Product-specific business modules",
)

PLUGGABLE_CAPABILITY_CONFIRMATIONS: Tuple[str, ...] = (
    "capability modules are organs/tools, not sovereign systems",
    "capability modules must use provider abstraction if provider-backed",
    "capability modules output candidate/evidence/signal, not direct fact/action/user output",
    "capability modules cannot bypass governance layer",
)

CONTROLLED_RUNTIME_CONFIRMATIONS: Tuple[str, ...] = (
    "controlled runtime framework is later admission framework",
    "simulation GO does not authorize runtime",
    "runtime requires admission / authorization / execution window / provider readiness / gate precondition / health supervision / evidence / rollback / post-review",
    "no real runtime opened now",
)

PRODUCT_FORMS: Tuple[str, ...] = (
    "Luna Badge",
    "Luna Glasses",
    "Phone",
    "Desktop",
    "Home Host / NAS",
    "Robot",
    "Cloud Luna",
)

PRODUCT_FORM_CONFIRMATIONS: Tuple[str, ...] = (
    "product form may change capabilities/hardware/providers",
    "product form cannot remove Seed Core",
    "product form cannot bypass governance standards",
    "product form must declare capability profile",
)

NO_UNIVERSAL_BRAIN_RULES: Tuple[str, ...] = (
    "Midplatform is not universal brain",
    "Midplatform is governance / coordination / routing / supervision system",
    "Information Integration Model cannot replace zones",
    "Decision Center cannot replace Constitution / Validation / Health",
    "Seed Core cannot become monolithic model",
    "Front models cannot bypass gates",
)

NO_MODULE_SOVEREIGNTY_RULES: Tuple[str, ...] = (
    "modules can have responsibility but not governance sovereignty",
    "modules cannot define their own constitution",
    "modules cannot self-authorize",
    "modules cannot auto-switch provider without policy",
    "modules cannot directly write Memory / WorldModel",
    "modules cannot directly emit user output",
    "modules cannot open runtime",
)

INVARIANT_BOUNDARIES: Tuple[str, ...] = (
    "Seed Core",
    "governance standards",
    "candidate/evidence semantics",
    "provider abstraction principle",
    "controlled runtime principle",
    "constitution/resolver/enforcement/health/whitebox principles",
    "no universal brain principle",
)

VARIANT_BOUNDARIES: Tuple[str, ...] = (
    "models",
    "providers",
    "sensors",
    "hardware",
    "runtime implementations",
    "product-specific modules",
    "business capabilities",
    "UI/output channels",
)

WORK_RHYTHM_CONFIRMATIONS: Tuple[str, ...] = (
    "do not expand validation phases unless required",
    "detection becomes reusable governance, not mainline expansion",
    "next phases focus on architecture stabilization and business mainline return",
    "Controlled Runtime completed as framework only",
    "no real runtime opened now",
)

RECOMMENDED_PHASE_SEQUENCE: Tuple[str, ...] = (
    "Midplatform vNext Architecture Realignment Planning",
    "Cognitive Zoning Architecture Planning",
    "Cognitive Zoning Architecture DryRunAndReview",
    "Seed Core / Pluggable Layer Architecture Planning",
    "Seed Core / Pluggable Layer Architecture DryRunAndReview",
    "Drive Signal Contract Planning",
    "Information Integration Layer Planning",
    "Return to First-Person Vision / Navigation Mainline",
)

DEFERRED_PHASES: Tuple[str, ...] = (
    "Seed Core / Pluggable Layer Architecture Planning",
    "Drive Signal Contract Planning",
    "Information Integration Layer Planning",
    "First-Person Vision / Navigation Mainline Recovery",
)

BLOCKED_ROUTES: Tuple[str, ...] = (
    "Direct OCR Runtime",
    "Direct TTS Runtime",
    "Direct Vision Runtime",
    "Direct Display Output Runtime",
    "Production Runtime",
)

DEFERRED_RUNTIMES: Tuple[str, ...] = (
    "OCR runtime deferred",
    "Vision runtime deferred",
    "ASR runtime deferred",
    "TTS runtime deferred",
    "Map provider runtime deferred",
    "Display Output runtime deferred",
    "Notification runtime deferred",
    "Voice-Audio runtime deferred",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Architecture Realignment Planning GO ≠ architecture implemented",
    "vNext layer model planned ≠ runtime enabled",
    "Seed Core positioned ≠ Seed Core runtime built",
    "Cognitive Zoning next ≠ universal brain creation",
    "deferred runtime ≠ cancelled runtime",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("architecture_realignment_planning_only",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "runtime_enabled_now",
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "controlled_runtime_execution_started_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
    "production_refactor_started_now",
    "file_migration_started_now",
    "cognitive_zoning_execution_started_now",
    "seed_core_runtime_enabled_now",
    "information_integration_runtime_enabled_now",
)

UPSTREAM_RUNTIME_LEAKAGE_FIELDS: Tuple[str, ...] = (
    "provider_invoked_now",
    "model_runtime_invoked_now",
    "controlled_runtime_enabled_now",
    "controlled_runtime_execution_started_now",
    "runtime_execution_window_opened_now",
    "tts_runtime_invoked_now",
    "display_output_invoked_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_vnext_architecture_realignment_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "system_level_simulated_go": True,
        "midplatform_vnext": True,
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


def _check_upstream_no_runtime_leakage(summary: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    for field in UPSTREAM_RUNTIME_LEAKAGE_FIELDS:
        if field in summary and summary.get(field) is not False:
            issues.append(f"{field} must be false")
    return issues


def run_midplatform_vnext_architecture_realignment_planning_v1(
    *,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    health_enforcement_supervisor_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_frontend_model_influence_simulation_dryrun_and_review_root: str,
    midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root: str,
    midplatform_display_gate_dryrun_and_review_root: str,
    midplatform_tts_runtime_dryrun_and_review_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    midplatform_whitebox_inspection_integration_dryrun_and_review_root: str,
    midplatform_controlled_runtime_planning_root: str,
    midplatform_speech_gate_dryrun_and_review_root: Optional[str] = None,
    midplatform_safety_gate_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    cr_dr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()
    health_dr_root = Path(health_enforcement_supervisor_dryrun_and_review_root).expanduser().resolve()
    provider_dr_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    fmis_dr_root = Path(
        midplatform_frontend_model_influence_simulation_dryrun_and_review_root
    ).expanduser().resolve()
    e2e_dr_root = Path(
        midplatform_end_to_end_output_chain_simulation_dryrun_and_review_root
    ).expanduser().resolve()
    display_dr_root = Path(midplatform_display_gate_dryrun_and_review_root).expanduser().resolve()
    tts_dr_root = Path(midplatform_tts_runtime_dryrun_and_review_root).expanduser().resolve()
    validation_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()
    whitebox_dr_root = Path(
        midplatform_whitebox_inspection_integration_dryrun_and_review_root
    ).expanduser().resolve()
    cr_plan_root = Path(midplatform_controlled_runtime_planning_root).expanduser().resolve()

    speech_dr_root = Path(
        midplatform_speech_gate_dryrun_and_review_root
        or "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_speech_gate_dryrun_and_review"
    ).expanduser().resolve()
    safety_dr_root = Path(
        midplatform_safety_gate_dryrun_and_review_root
        or "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review"
    ).expanduser().resolve()

    cr_dr_sm = _try_read_json(cr_dr_root / "summary.json") or {}
    cr_dr_vr = _try_read_json(cr_dr_root / "verifier_report.json") or {}
    health_dr_vr = _try_read_json(health_dr_root / "verifier_report.json") or {}
    provider_dr_vr = _try_read_json(provider_dr_root / "verifier_report.json") or {}
    provider_dr_sm = _try_read_json(provider_dr_root / "summary.json") or {}
    fmis_dr_vr = _try_read_json(fmis_dr_root / "verifier_report.json") or {}
    fmis_dr_sm = _try_read_json(fmis_dr_root / "summary.json") or {}
    e2e_dr_vr = _try_read_json(e2e_dr_root / "verifier_report.json") or {}
    e2e_dr_sm = _try_read_json(e2e_dr_root / "summary.json") or {}
    display_dr_vr = _try_read_json(display_dr_root / "verifier_report.json") or {}
    speech_dr_vr = _try_read_json(speech_dr_root / "verifier_report.json") or {}
    safety_dr_vr = _try_read_json(safety_dr_root / "verifier_report.json") or {}
    tts_dr_vr = _try_read_json(tts_dr_root / "verifier_report.json") or {}
    validation_dr_vr = _try_read_json(validation_dr_root / "verifier_report.json") or {}
    whitebox_dr_vr = _try_read_json(whitebox_dr_root / "verifier_report.json") or {}
    cr_plan_vr = _try_read_json(cr_plan_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_controlled_runtime_dryrun_root": str(cr_dr_root),
        "upstream_health_supervisor_dryrun_root": str(health_dr_root),
        "upstream_provider_abstraction_dryrun_root": str(provider_dr_root),
        "upstream_fmis_dryrun_root": str(fmis_dr_root),
        "upstream_e2e_simulation_dryrun_root": str(e2e_dr_root),
        "upstream_display_gate_dryrun_root": str(display_dr_root),
        "upstream_speech_gate_dryrun_root": str(speech_dr_root),
        "upstream_safety_gate_dryrun_root": str(safety_dr_root),
        "upstream_tts_runtime_dryrun_root": str(tts_dr_root),
        "upstream_validation_dryrun_root": str(validation_dr_root),
        "upstream_whitebox_dryrun_root": str(whitebox_dr_root),
        "upstream_controlled_runtime_planning_root": str(cr_plan_root),
        "output_root": str(out_root),
    }

    if cr_dr_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime DryRunAndReview verifier must be GO")
    if cr_dr_sm.get("final_decision") != UPSTREAM_CONTROLLED_RUNTIME_DR_FINAL:
        blockers.append("controlled runtime dryrun final_decision mismatch")
    if health_dr_vr.get("verifier") != "GO":
        blockers.append("Health Enforcement Supervisor DryRunAndReview must be GO")
    if provider_dr_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction DryRunAndReview must be GO")
    if provider_dr_sm.get("final_decision") != PROVIDER_ABS_DR_FINAL_GO:
        blockers.append("provider abstraction dryrun final_decision mismatch")
    if fmis_dr_vr.get("verifier") != "GO":
        blockers.append("FMIS DryRunAndReview must be GO")
    if fmis_dr_sm.get("final_decision") != FMIS_DR_FINAL_GO:
        blockers.append("FMIS dryrun final_decision mismatch")
    if e2e_dr_vr.get("verifier") != "GO":
        blockers.append("E2E Simulation DryRunAndReview must be GO")
    if e2e_dr_sm.get("final_decision") != E2E_DR_FINAL_GO:
        blockers.append("E2E simulation dryrun final_decision mismatch")
    if display_dr_vr.get("verifier") != "GO":
        blockers.append("Display Gate DryRunAndReview must be GO")
    if speech_dr_vr.get("verifier") != "GO":
        blockers.append("Speech Gate DryRunAndReview must be GO")
    if safety_dr_vr.get("verifier") != "GO":
        blockers.append("Safety Gate DryRunAndReview must be GO")
    if tts_dr_vr.get("verifier") != "GO":
        blockers.append("TTS Runtime DryRunAndReview must be GO")
    if validation_dr_vr.get("verifier") != "GO":
        blockers.append("Validation Engineering Separation DryRunAndReview must be GO")
    if whitebox_dr_vr.get("verifier") != "GO":
        blockers.append("Whitebox Inspection Integration DryRunAndReview must be GO")
    if cr_plan_vr.get("verifier") != "GO":
        blockers.append("Controlled Runtime Planning must be GO")

    leakage_issues: List[str] = []
    for label, sm in (
        ("controlled_runtime_dr", cr_dr_sm),
        ("health_supervisor", _try_read_json(health_dr_root / "summary.json") or {}),
        ("provider_abstraction", provider_dr_sm),
        ("fmis", fmis_dr_sm),
        ("e2e", e2e_dr_sm),
        ("display_gate", _try_read_json(display_dr_root / "summary.json") or {}),
        ("speech_gate", _try_read_json(speech_dr_root / "summary.json") or {}),
        ("safety_gate", _try_read_json(safety_dr_root / "summary.json") or {}),
        ("tts", _try_read_json(tts_dr_root / "summary.json") or {}),
        ("whitebox", _try_read_json(whitebox_dr_root / "summary.json") or {}),
    ):
        for issue in _check_upstream_no_runtime_leakage(sm):
            leakage_issues.append(f"{label}:{issue}")
    blockers.extend(leakage_issues)

    input_ok = len(blockers) == 0

    closure_input_review = {
        "review_id": "controlled_runtime_closure_input_review_v1",
        "controlled_runtime_dryrun_verifier": cr_dr_vr.get("verifier"),
        "controlled_runtime_dryrun_final_decision": cr_dr_sm.get("final_decision"),
        "system_level_simulated_go": True,
        "no_runtime_leakage_in_upstream": len(leakage_issues) == 0,
        "architecture_realignment_planning_only": True,
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    layer_model = {
        "model_id": "midplatform_vnext_layer_model_v1",
        "architecture_name": "Luna Midplatform vNext",
        "layer_count": len(VNEXT_LAYERS),
        "layers": list(VNEXT_LAYERS),
        **meta,
    }

    seed_core = {
        "positioning_id": "fixed_seed_core_positioning_v1",
        "components": list(SEED_CORE_COMPONENTS),
        "component_count": len(SEED_CORE_COMPONENTS),
        "fixed_invariant": True,
        "confirmations": list(SEED_CORE_CONFIRMATIONS),
        **meta,
    }

    governance_layer = {
        "layer_id": "reusable_governance_standard_layer_v1",
        "standards": list(GOVERNANCE_STANDARDS),
        "standard_count": len(GOVERNANCE_STANDARDS),
        "confirmations": list(GOVERNANCE_STANDARD_CONFIRMATIONS),
        **meta,
    }

    cognitive_zoning = {
        "positioning_id": "cognitive_zoning_positioning_v1",
        "zones": list(COGNITIVE_ZONES),
        "zone_count": len(COGNITIVE_ZONES),
        "confirmations": list(COGNITIVE_ZONING_CONFIRMATIONS),
        **meta,
    }

    pluggable_layer = {
        "positioning_id": "pluggable_capability_layer_positioning_v1",
        "capability_types": list(PLUGGABLE_CAPABILITY_TYPES),
        "confirmations": list(PLUGGABLE_CAPABILITY_CONFIRMATIONS),
        **meta,
    }

    controlled_runtime_layer = {
        "positioning_id": "controlled_runtime_layer_positioning_v1",
        "confirmations": list(CONTROLLED_RUNTIME_CONFIRMATIONS),
        "runtime_opened_now": False,
        **meta,
    }

    product_form_layer = {
        "positioning_id": "product_form_layer_positioning_v1",
        "product_forms": list(PRODUCT_FORMS),
        "form_count": len(PRODUCT_FORMS),
        "confirmations": list(PRODUCT_FORM_CONFIRMATIONS),
        **meta,
    }

    no_universal_brain = {
        "policy_id": "no_universal_midplatform_brain_policy_v1",
        "rules": list(NO_UNIVERSAL_BRAIN_RULES),
        "rule_count": len(NO_UNIVERSAL_BRAIN_RULES),
        **meta,
    }

    no_module_sovereignty = {
        "policy_id": "no_module_sovereignty_policy_v1",
        "rules": list(NO_MODULE_SOVEREIGNTY_RULES),
        "rule_count": len(NO_MODULE_SOVEREIGNTY_RULES),
        **meta,
    }

    invariant_variant_matrix = {
        "matrix_id": "invariant_vs_variant_boundary_matrix_v1",
        "invariant": list(INVARIANT_BOUNDARIES),
        "variant": list(VARIANT_BOUNDARIES),
        "invariant_count": len(INVARIANT_BOUNDARIES),
        "variant_count": len(VARIANT_BOUNDARIES),
        **meta,
    }

    work_rhythm = {
        "plan_id": "post_detection_work_rhythm_plan_v1",
        "confirmations": list(WORK_RHYTHM_CONFIRMATIONS),
        "recommended_sequence": list(RECOMMENDED_PHASE_SEQUENCE),
        "sequence_count": len(RECOMMENDED_PHASE_SEQUENCE),
        **meta,
    }

    downstream_sequence = {
        "decision_id": "downstream_phase_sequence_decision_v1",
        "selected_next_phase": NEXT_PHASE_GO,
        "deferred_phases": list(DEFERRED_PHASES),
        "blocked_routes": list(BLOCKED_ROUTES),
        "blocked_count": len(BLOCKED_ROUTES),
        "deferred_count": len(DEFERRED_PHASES),
        **meta,
    }

    deferred_runtime_register = {
        "register_id": "deferred_runtime_register_v1",
        "deferred_runtimes": list(DEFERRED_RUNTIMES),
        "deferred_count": len(DEFERRED_RUNTIMES),
        "deferred_not_cancelled": True,
        **meta,
    }

    planning_pass = input_ok

    realignment_decision = {
        "decision_id": "midplatform_vnext_architecture_realignment_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "architecture_realignment_summary": [
            "Fixed Seed Core (Layer 0) — invariant life kernel",
            "Reusable Governance Standard Layer (Layer 1) — common standards not module sovereignty",
            "Cognitive Zoning Layer (Layer 2) — no universal brain",
            "Information Integration / Decision (Layer 3)",
            "Pluggable Capability Layer (Layer 4)",
            "Controlled Runtime Layer (Layer 5) — framework only, not execution now",
            "Product Form Layer (Layer 6)",
        ],
        **meta,
    }

    policy = {
        "policy_id": "midplatform_vnext_architecture_realignment_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "midplatform_vnext": True,
        "not_runtime_not_refactor": True,
        "layer_count": 7,
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
        "final_decision": realignment_decision["final_decision"],
        "recommended_next_phase": realignment_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "midplatform_vnext_architecture_realignment_policy": policy,
        "controlled_runtime_closure_input_review": closure_input_review,
        "midplatform_vnext_layer_model": layer_model,
        "fixed_seed_core_positioning": seed_core,
        "reusable_governance_standard_layer": governance_layer,
        "cognitive_zoning_positioning": cognitive_zoning,
        "pluggable_capability_layer_positioning": pluggable_layer,
        "controlled_runtime_layer_positioning": controlled_runtime_layer,
        "product_form_layer_positioning": product_form_layer,
        "no_universal_midplatform_brain_policy": no_universal_brain,
        "no_module_sovereignty_policy": no_module_sovereignty,
        "invariant_vs_variant_boundary_matrix": invariant_variant_matrix,
        "post_detection_work_rhythm_plan": work_rhythm,
        "downstream_phase_sequence_decision": downstream_sequence,
        "deferred_runtime_register": deferred_runtime_register,
        "non_claims_register": non_claims,
        "midplatform_vnext_architecture_realignment_decision": realignment_decision,
        "summary": summary,
    }
