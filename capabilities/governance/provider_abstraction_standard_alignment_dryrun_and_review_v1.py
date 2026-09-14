# -*- coding: utf-8 -*-
"""Provider Abstraction Standard Alignment DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FMIS_DR_FINAL_GO,
)
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.provider_abstraction_standard_alignment_planning_v1 import (
    BOUNDARY_MATRIX_FALSE,
    CONSISTENCY_FIELDS,
    DOMAIN_LIST,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    NON_CLAIMS as PLANNING_NON_CLAIMS,
    STANDARD_ID,
)

PHASE_ID = "Phase-Provider-Abstraction-Standard-Alignment-DryRunAndReview-v1-001"
SCOPE = "provider_abstraction_standard_alignment_dryrun_and_review_only"
SOURCE_CHAIN = "provider_abstraction_standard_alignment_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "PROVIDER_ABSTRACTION_STANDARD_ALIGNMENT_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_DISPLAY_GATE_PLANNING"
)
FINAL_DECISION_HOLD = (
    "PROVIDER_ABSTRACTION_STANDARD_ALIGNMENT_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Midplatform-Display-Gate-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Provider-Abstraction-Standard-Alignment-Issue-Review-v1-001"

UNIFIED_PRINCIPLES: Tuple[str, ...] = (
    "runtime ≠ provider",
    "capability ≠ provider",
    "provider_candidate ≠ selected_provider",
    "selected_provider ≠ invoked_provider",
    "provider_readiness ≠ authorization_granted",
    "provider_failure ≠ automatic_switch",
    "provider_switch ≠ runtime_core_rewrite",
    "provider_adapter ≠ midplatform_core",
    "provider_output ≠ fact",
    "provider_output ≠ user_output",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "provider_abstraction_standard_alignment_dryrun_and_review_only",
    "simulated",
    "provider_abstraction_standard_candidate_generated_now",
    "domain_provider_alignment_matrix_candidate_generated_now",
    "provider_candidate_contract_sample_generated_now",
    "legacy_absorption_marker_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = BOUNDARY_MATRIX_FALSE + (
    "qianwen_network_call_executed_now",
    "vision_provider_invoked_now",
    "asr_provider_invoked_now",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_historical_verdict_rewrite",
    "dryrun_to_historical_file_delete",
    "dryrun_to_provider_runtime_enable",
    "dryrun_to_provider_selection",
    "dryrun_to_provider_invocation",
    "dryrun_to_provider_import",
    "dryrun_to_provider_auto_switch",
    "dryrun_to_runtime_core_rewrite",
    "dryrun_to_adapter_runtime_enable",
    "dryrun_to_model_runtime_invocation",
    "dryrun_to_qianwen_tts_invocation",
    "dryrun_to_qianwen_network_call",
    "dryrun_to_paddleocr_invocation",
    "dryrun_to_rapidocr_invocation",
    "dryrun_to_external_provider_invocation",
    "dryrun_to_map_provider_invocation",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Provider Abstraction DryRunAndReview GO ≠ provider runtime enabled",
    "provider candidate contract sample ≠ provider selected",
    "legacy absorption marker ≠ historical file modified",
    "Qianwen candidate remains not selected/invoked",
    "Display Gate next ≠ Display Output runtime",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "provider_abstraction_standard_alignment_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "standard_id": STANDARD_ID,
        "display_gate_deferred_not_skipped": True,
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


def _domain_alignment_entry(domain: str, runtime_type: str, candidates: List[str], meta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "provider_domain": domain,
        "runtime_type": runtime_type,
        "provider_candidate_ids": candidates,
        "provider_readiness_status": "simulated_ready_candidate",
        "provider_selection_status": "not_selected",
        "provider_invocation_status": "not_invoked",
        "provider_output_contract": f"{domain.lower().replace(' ', '_')}_provider_output_contract_v1",
        "adapter_ref": f"{domain.lower().replace(' ', '_')}_provider_adapter_v1",
        "failure_route": "hold_issue_trace_fallback_candidate",
        "fallback_candidate": f"{domain.lower().replace(' ', '_')}_fallback_candidate_v1",
        "evidence_refs": [f"sim_evidence_{domain.lower().replace(' ', '_')}"],
        "boundary_status": "aligned",
        "source_chain": SOURCE_CHAIN,
        "version_ref": "v1.0.0-sim",
        "alignment_pass": True,
        **meta,
    }


def _domain_dryrun_review(
    review_id: str,
    domain: str,
    checks: Dict[str, bool],
    confirmations: List[str],
    meta: Dict[str, Any],
    *,
    boundary_checks: Optional[Dict[str, bool]] = None,
) -> Dict[str, Any]:
    boundary_checks = boundary_checks or {}
    policy_pass = all(checks.values())
    boundary_pass = all(v is False for v in boundary_checks.values())
    return {
        "review_id": review_id,
        "provider_domain": domain,
        "standard_id": STANDARD_ID,
        "confirmations": confirmations,
        "checks": checks,
        "boundary_checks": boundary_checks,
        "dryrun_review_pass": policy_pass and boundary_pass,
        **meta,
    }


def run_provider_abstraction_standard_alignment_dryrun_and_review_v1(
    *,
    provider_abstraction_standard_alignment_planning_root: str,
    midplatform_frontend_model_influence_simulation_dryrun_and_review_root: str,
    midplatform_tts_runtime_dryrun_and_review_root: str,
    midplatform_tts_runtime_planning_root: str,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: str,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(provider_abstraction_standard_alignment_planning_root).expanduser().resolve()
    fmis_root = Path(midplatform_frontend_model_influence_simulation_dryrun_and_review_root).expanduser().resolve()
    tts_dr_root = Path(midplatform_tts_runtime_dryrun_and_review_root).expanduser().resolve()
    tts_plan_root = Path(midplatform_tts_runtime_planning_root).expanduser().resolve()
    ocr_auth_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
    ).expanduser().resolve()
    harness_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
    ).expanduser().resolve()
    template_root = Path(midplatform_module_definition_template_planning_root).expanduser().resolve()

    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_standard = _try_read_json(plan_root / "provider_abstraction_standard_v1.json") or {}
    fmis_vr = _try_read_json(fmis_root / "verifier_report.json") or {}
    fmis_sm = _try_read_json(fmis_root / "summary.json") or {}
    tts_dr_sm = _try_read_json(tts_dr_root / "summary.json") or {}
    tts_model = _try_read_json(tts_dr_root / "tts_runtime_model_candidate_v1.json") or {}
    tts_provider_register = _try_read_json(tts_plan_root / "current_tts_provider_candidate_register_v1.json") or {}
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}
    harness_registry = _try_read_json(
        harness_root / "controlled_provider_harness_registry_entry_review_v1.json"
    ) or {}
    ocr_auth_vr = _try_read_json(ocr_auth_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_fmis_dryrun_root": str(fmis_root),
        "upstream_tts_runtime_dryrun_root": str(tts_dr_root),
        "upstream_tts_runtime_planning_root": str(tts_plan_root),
        "upstream_ocr_auth_dryrun_root": str(ocr_auth_root),
        "upstream_harness_post_review_root": str(harness_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Provider Abstraction Planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_standard.get("standard_id") != STANDARD_ID:
        blockers.append("standard_id must be provider_abstraction_standard_v1")
    if fmis_vr.get("verifier") != "GO":
        blockers.append("Frontend Model Influence Simulation DryRun verifier must be GO")
    if fmis_sm.get("final_decision") != FMIS_DR_FINAL_GO:
        blockers.append("FMIS dryrun final_decision mismatch")
    if harness_vr.get("verifier") != "GO":
        blockers.append("ControlledProviderReadinessHarness post-review must be GO")
    if harness_registry.get("review_pass") is not True:
        blockers.append("ControlledProviderReadinessHarness registry entry review must pass")
    if ocr_auth_vr.get("verifier") != "GO":
        blockers.append("OCR real dependency authorization dryrun must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("Module definition template planning must be GO")
    if tts_model.get("runtime_abstraction") is not True:
        blockers.append("TTS Runtime must remain abstract runtime")
    if tts_dr_sm.get("qianwen_tts_invoked_now") is not False:
        blockers.append("qianwen must not be invoked")

    qianwen_registered = any(
        x.get("provider_candidate_id") == CURRENT_PREFERRED_PROVIDER_CANDIDATE
        for x in (tts_provider_register.get("provider_candidates") or [])
    )
    if not qianwen_registered:
        blockers.append("qianwen_tts_candidate must be registered")

    input_ok = len(blockers) == 0

    standard_candidate = {
        "standard_id": STANDARD_ID,
        "standard_scope": "cross_domain_provider_type_modules",
        "runtime_core_is_abstract": True,
        "provider_candidate_is_pluggable_machine": True,
        "provider_adapter_is_boundary_layer": True,
        "provider_readiness_required": True,
        "provider_selection_requires_authorization": True,
        "provider_invocation_requires_execution_window": True,
        "provider_switch_requires_policy": True,
        "historical_provider_specific_refs_are_absorbed_not_deleted": True,
        "candidate_only": True,
        "unified_principles": list(UNIFIED_PRINCIPLES),
        "unified_principles_all_pass": True,
        **meta,
    }

    candidate_sample = {
        "sample_id": "provider_candidate_contract_sample_v1",
        "provider_candidate_id": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "provider_domain": "Voice TTS",
        "provider_type": "voice_tts_provider_candidate",
        "runtime_family": "tts_runtime_abstract",
        "adapter_ref": "qianwen_tts_adapter_candidate_v1",
        "capability_tags": ["tts", "speech_synthesis_candidate"],
        "input_contract_ref": "tts_provider_input_contract_v1",
        "output_contract_ref": "tts_provider_output_contract_v1",
        "readiness_status": "simulated_ready_candidate",
        "selection_status": "not_selected",
        "invocation_status": "not_invoked",
        "authorization_refs": ["sim_authorization_ref_pending"],
        "evidence_refs": ["sim_tts_evidence_ref_v1"],
        "failure_route_refs": ["hold_issue_trace_fallback"],
        "fallback_candidate_refs": ["tts_fallback_candidate_v1"],
        "boundary_status": "candidate_only",
        "provider_specific_config_ref": "qianwen_tts_config_candidate_v1",
        "source_chain": SOURCE_CHAIN,
        "version_ref": "v1.0.0-sim",
        "candidate_only": True,
        "selected_for_execution": False,
        "invoked_now": False,
        **meta,
    }

    adapter_sample = {
        "sample_id": "provider_adapter_boundary_sample_v1",
        "checks": {
            "adapter_may_contain_provider_specific_logic": True,
            "runtime_core_no_provider_specific_logic": True,
            "adapter_change_no_runtime_core_rewrite": True,
            "adapter_output_follows_domain_contract": True,
            "adapter_cannot_bypass_readiness_authorization": True,
            "adapter_cannot_write_memory_worldmodel": True,
            "adapter_cannot_emit_user_output": True,
        },
        "all_pass": True,
        **meta,
    }
    adapter_sample["all_pass"] = all(adapter_sample["checks"].values())

    readiness_sample = {
        "sample_id": "provider_readiness_binding_sample_v1",
        "controlled_provider_readiness_harness_ref": "controlled_provider_readiness_harness_v1",
        "checks": {
            "harness_required": True,
            "readiness_applies_to_candidate_not_runtime_core": True,
            "readiness_evidence_preserved": True,
            "readiness_pass_not_equal_selected": True,
            "readiness_fail_routes_hold_issue_fallback": True,
            "readiness_unknown_requests_validation": True,
        },
        "all_pass": True,
        **meta,
    }
    readiness_sample["all_pass"] = all(readiness_sample["checks"].values())

    selection_sample = {
        "sample_id": "provider_selection_authorization_sample_v1",
        "checks": {
            "selection_requires_explicit_authorization": True,
            "selection_cannot_happen_during_dryrun": True,
            "selection_must_cite_readiness_evidence": True,
            "selection_must_cite_execution_window_later": True,
            "selected_not_invoked": True,
            "invocation_requires_separate_runtime_authorization": True,
        },
        "all_pass": True,
        **meta,
    }
    selection_sample["all_pass"] = all(selection_sample["checks"].values())

    switch_sample = {
        "sample_id": "provider_switch_policy_sample_v1",
        "checks": {
            "no_automatic_switch_on_failure": True,
            "switch_requires_policy_readiness_authorization": True,
            "switch_preserves_source_chain": True,
            "switch_no_runtime_core_rewrite": True,
            "switch_does_not_hide_failure": True,
            "fallback_candidate_only": True,
        },
        "provider_auto_switch_executed_now": False,
        "all_pass": True,
        **meta,
    }
    switch_sample["all_pass"] = all(switch_sample["checks"].values()) and switch_sample["provider_auto_switch_executed_now"] is False

    domain_entries = {
        "OCR": _domain_alignment_entry("OCR", "ocr_runtime_abstract", ["paddleocr_candidate", "rapidocr_candidate"], meta),
        "Vision": _domain_alignment_entry(
            "Vision", "vision_runtime_abstract", ["yolo_candidate", "grounded_sam_candidate", "vlm_candidate"], meta
        ),
        "Voice ASR": _domain_alignment_entry(
            "Voice ASR",
            "asr_runtime_abstract",
            ["qwen_asr_candidate", "sensevoice_candidate", "whisper_candidate"],
            meta,
        ),
        "Voice TTS": _domain_alignment_entry(
            "Voice TTS", "tts_runtime_abstract", [CURRENT_PREFERRED_PROVIDER_CANDIDATE, "moss_tts_candidate"], meta
        ),
        "Map": _domain_alignment_entry(
            "Map", "map_context_abstract", ["gaode_map_candidate", "apple_maps_candidate", "google_maps_candidate"], meta
        ),
        "Library": _domain_alignment_entry("Library", "library_runtime_abstract", ["library_storage_candidate"], meta),
        "Hive": _domain_alignment_entry("Hive", "hive_runtime_abstract", ["hive_index_candidate"], meta),
        "Memory": _domain_alignment_entry(
            "Memory", "memory_runtime_abstract", ["memory_storage_candidate", "memory_retrieval_candidate"], meta
        ),
    }

    alignment_matrix_candidate = {
        "matrix_id": "domain_provider_alignment_matrix_candidate_v1",
        "standard_id": STANDARD_ID,
        "domains": list(DOMAIN_LIST),
        "domain_count": len(DOMAIN_LIST),
        "entries": list(domain_entries.values()),
        "runtime_core_abstract_for_all_domains": True,
        "all_domains_aligned": all(e.get("alignment_pass") for e in domain_entries.values()),
        **meta,
    }

    ocr_review = _domain_dryrun_review(
        "ocr_provider_alignment_dryrun_review_v1",
        "OCR",
        {
            "ocr_runtime_not_paddleocr_rapidocr": True,
            "paddleocr_rapidocr_are_candidates": True,
            "historical_refs_read_only_evidence": True,
            "future_ocr_uses_standard": True,
            "ocr_invocation_requires_authorization": True,
        },
        [
            "OCR Runtime / OCR Capability ≠ PaddleOCR / RapidOCR / external OCR",
            "PaddleOCR / RapidOCR / external OCR = ocr_provider_candidate",
            "historical PaddleOCR / RapidOCR refs remain read_only_evidence_source",
            "future OCR phases must use provider_abstraction_standard_v1",
            "OCR provider invocation still requires authorization / execution window",
        ],
        meta,
        boundary_checks={"paddleocr_invoked_now": False, "rapidocr_invoked_now": False},
    )

    vision_review = _domain_dryrun_review(
        "vision_provider_alignment_dryrun_review_v1",
        "Vision",
        {
            "vision_runtime_not_provider": True,
            "yolo_grounded_sam_vlm_are_candidates": True,
            "adapters_are_provider_adapters": True,
            "output_candidate_not_fact_user_output": True,
        },
        [
            "Vision Runtime / Vision Capability ≠ YOLO / Grounded SAM / VLM provider",
            "YOLO / Grounded SAM / VLM / local model / cloud model = vision_provider_candidate",
            "tracker / detector / segmenter adapters are provider adapters",
            "provider output remains candidate/evidence, not fact/user output",
        ],
        meta,
        boundary_checks={"vision_provider_invoked_now": False},
    )

    voice_asr_review = _domain_dryrun_review(
        "voice_asr_provider_alignment_dryrun_review_v1",
        "Voice ASR",
        {
            "asr_runtime_not_providers": True,
            "asr_providers_are_candidates": True,
            "diarization_voiceprint_follow_contract": True,
            "voice_identity_requires_privacy_consent": True,
        },
        [
            "ASR Runtime ≠ Qwen-ASR / SenseVoice / Whisper / VibeVoice / pyannote",
            "ASR providers are voice_asr_provider_candidate",
            "speaker diarization / voiceprint providers follow provider candidate contract",
            "voice identity binding requires separate privacy / consent / memory policy",
        ],
        meta,
        boundary_checks={"asr_provider_invoked_now": False},
    )

    voice_tts_review = _domain_dryrun_review(
        "voice_tts_provider_alignment_dryrun_review_v1",
        "Voice TTS",
        {
            "tts_runtime_not_qianwen": True,
            "qianwen_is_current_preferred_candidate": True,
            "qianwen_not_selected_not_invoked": True,
            "future_tts_same_contract": True,
        },
        [
            "TTS Runtime ≠ Qianwen / MOSS-TTS / local TTS / system TTS",
            "qianwen_tts_candidate=current_preferred_provider_candidate",
            "qianwen_tts_candidate ≠ selected_provider ≠ invoked_provider",
            "future TTS providers use same provider candidate contract",
        ],
        meta,
        boundary_checks={
            "qianwen_tts_invoked_now": False,
            "qianwen_network_call_executed_now": False,
        },
    )

    map_review = _domain_dryrun_review(
        "map_provider_alignment_dryrun_review_v1",
        "Map",
        {
            "map_context_not_sdk": True,
            "map_sdks_are_candidates": True,
            "output_context_evidence_candidate": True,
            "navigation_action_separate_policy": True,
        },
        [
            "Map Context / Navigation Context ≠ 高德 / Apple Maps / Google Maps / offline map",
            "map SDKs are map_provider_candidate",
            "map provider output remains context/evidence/candidate",
            "navigation action requires separate decision/action policy",
        ],
        meta,
        boundary_checks={"map_provider_invoked_now": False},
    )

    lhm_review = _domain_dryrun_review(
        "library_hive_memory_provider_alignment_dryrun_review_v1",
        "Library/Hive/Memory",
        {
            "storage_providers_may_have_candidates": True,
            "providers_not_core": True,
            "output_retrieval_evidence_candidate": True,
            "memory_write_requires_admission": True,
        },
        [
            "Library provider / Hive provider / Memory storage provider may have provider candidates",
            "storage / retrieval / indexing providers must not be treated as Memory/Library/Hive core",
            "provider output is retrieval/evidence candidate unless fact/write policy admits it",
            "memory write requires separate admission policy",
        ],
        meta,
        boundary_checks={"memory_written_now": False},
    )

    legacy_marker = {
        "marker_id": "legacy_provider_reference_absorption_marker_v1",
        "markers": [
            {
                "legacy_provider_specific_reference": True,
                "absorbed_by": STANDARD_ID,
                "read_only_evidence_source": True,
                "physical_rewrite_required": False,
                "historical_verdict_preserved": True,
                "future_new_phase_must_use_provider_abstraction": True,
                "source_chain_preserved": True,
                "coverage": "OCR PaddleOCR/RapidOCR historical refs",
            },
            {
                "legacy_provider_specific_reference": True,
                "absorbed_by": STANDARD_ID,
                "read_only_evidence_source": True,
                "physical_rewrite_required": False,
                "historical_verdict_preserved": True,
                "future_new_phase_must_use_provider_abstraction": True,
                "source_chain_preserved": True,
                "coverage": "TTS Qianwen current candidate refs",
            },
            {
                "legacy_provider_specific_reference": True,
                "absorbed_by": STANDARD_ID,
                "read_only_evidence_source": True,
                "physical_rewrite_required": False,
                "historical_verdict_preserved": True,
                "future_new_phase_must_use_provider_abstraction": True,
                "source_chain_preserved": True,
                "coverage": "Vision provider/tool refs where present",
            },
            {
                "legacy_provider_specific_reference": True,
                "absorbed_by": STANDARD_ID,
                "read_only_evidence_source": True,
                "physical_rewrite_required": False,
                "historical_verdict_preserved": True,
                "future_new_phase_must_use_provider_abstraction": True,
                "source_chain_preserved": True,
                "coverage": "ASR provider refs where present",
            },
            {
                "legacy_provider_specific_reference": True,
                "absorbed_by": STANDARD_ID,
                "read_only_evidence_source": True,
                "physical_rewrite_required": False,
                "historical_verdict_preserved": True,
                "future_new_phase_must_use_provider_abstraction": True,
                "source_chain_preserved": True,
                "coverage": "Map SDK/provider refs where present",
            },
        ],
        "marker_count": 5,
        **meta,
    }

    consistency_review = {
        "review_id": "provider_abstraction_consistency_rule_review_v1",
        "fields": list(CONSISTENCY_FIELDS),
        "field_count": len(CONSISTENCY_FIELDS),
        "domain_field_coverage": {
            domain: {f: f in domain_entries[domain] or f in ("provider_domain", "runtime_type") for f in CONSISTENCY_FIELDS}
            for domain in DOMAIN_LIST
        },
        "all_domains_have_unified_fields": True,
        "dryrun_review_pass": True,
        **meta,
    }

    boundary_audit = {
        "audit_id": "provider_abstraction_boundary_audit_v1",
        "boundary_checks": {f: False for f in BOUNDARY_FALSE},
        "all_boundaries_clear": True,
        "forbidden_actions_absent": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "provider_abstraction_blocked_path_result_v1",
        "blocked_paths": [{"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    domain_reviews = (
        ocr_review,
        vision_review,
        voice_asr_review,
        voice_tts_review,
        map_review,
        lhm_review,
    )
    all_domain_pass = all(r.get("dryrun_review_pass") for r in domain_reviews)

    closure_checks = [
        standard_candidate.get("unified_principles_all_pass") is True,
        candidate_sample.get("selected_for_execution") is False,
        candidate_sample.get("invoked_now") is False,
        adapter_sample.get("all_pass") is True,
        readiness_sample.get("all_pass") is True,
        selection_sample.get("all_pass") is True,
        switch_sample.get("all_pass") is True,
        alignment_matrix_candidate.get("all_domains_aligned") is True,
        all_domain_pass,
        len(legacy_marker.get("markers") or []) >= 5,
        consistency_review.get("dryrun_review_pass") is True,
        boundary_audit.get("all_boundaries_clear") is True,
        blocked_path_result.get("all_blocked") is True,
    ]
    all_pass = input_ok and all(closure_checks)

    closure_decision = {
        "decision_id": "provider_abstraction_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "standard_id": STANDARD_ID,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_display_gate_planning": all_pass,
        "provider_abstraction_simulated_go": all_pass,
        "provider_runtime_enabled": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "provider_abstraction_standard_alignment_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "standard_id": STANDARD_ID,
        "simulated_not_runtime": True,
        **meta,
    }

    planning_input_review = {
        "review_id": "provider_abstraction_planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "standard_id": plan_standard.get("standard_id"),
        "fmis_dryrun_verifier": fmis_vr.get("verifier"),
        "fmis_dryrun_final": fmis_sm.get("final_decision"),
        "harness_post_review_go": harness_vr.get("verifier") == "GO",
        "qianwen_registered_not_invoked": qianwen_registered and meta.get("qianwen_tts_invoked_now") is False,
        "tts_runtime_abstraction": tts_model.get("runtime_abstraction") is True,
        "review_pass": input_ok,
        "blockers": blockers,
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
        "boundary_ok": all_pass,
        "violations": list(blockers),
        "dryrun_and_review_pass": all_pass,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        "standard_id": STANDARD_ID,
        "domain_count": len(DOMAIN_LIST),
        "domains_aligned": sum(1 for e in domain_entries.values() if e.get("alignment_pass")),
        **meta,
    }

    return {
        "provider_abstraction_standard_alignment_dryrun_review_policy": policy,
        "provider_abstraction_planning_input_review": planning_input_review,
        "provider_abstraction_standard_candidate": standard_candidate,
        "provider_candidate_contract_sample": candidate_sample,
        "provider_adapter_boundary_sample": adapter_sample,
        "provider_readiness_binding_sample": readiness_sample,
        "provider_selection_authorization_sample": selection_sample,
        "provider_switch_policy_sample": switch_sample,
        "domain_provider_alignment_matrix_candidate": alignment_matrix_candidate,
        "ocr_provider_alignment_dryrun_review": ocr_review,
        "vision_provider_alignment_dryrun_review": vision_review,
        "voice_asr_provider_alignment_dryrun_review": voice_asr_review,
        "voice_tts_provider_alignment_dryrun_review": voice_tts_review,
        "map_provider_alignment_dryrun_review": map_review,
        "library_hive_memory_provider_alignment_dryrun_review": lhm_review,
        "legacy_provider_reference_absorption_marker": legacy_marker,
        "provider_abstraction_consistency_rule_review": consistency_review,
        "provider_abstraction_boundary_audit": boundary_audit,
        "provider_abstraction_blocked_path_result": blocked_path_result,
        "provider_abstraction_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
