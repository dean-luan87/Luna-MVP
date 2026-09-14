# -*- coding: utf-8 -*-
"""Provider Abstraction Standard Alignment Planning v1.

Planning-only cross-domain governance. This phase defines a unified abstraction standard
for provider-type modules without rewriting historical evidence, rerunning old phases,
or invoking any providers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_post_output_chain_simulation_roadmap_decision_v1 import (
    FINAL_DECISION_GO as UPSTREAM_ROADMAP_FINAL_GO,
    ROUTE_A as ROUTE_A_LABEL,
)
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Provider-Abstraction-Standard-Alignment-Planning-v1-001"
SCOPE = "provider_abstraction_standard_alignment_planning_only"
SOURCE_CHAIN = "provider_abstraction_standard_alignment_planning_v1"

FINAL_DECISION_GO = "PROVIDER_ABSTRACTION_STANDARD_ALIGNMENT_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
FINAL_DECISION_HOLD = "PROVIDER_ABSTRACTION_STANDARD_ALIGNMENT_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Provider-Abstraction-Standard-Alignment-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Provider-Abstraction-Standard-Alignment-Issue-Review-v1-001"

STANDARD_ID = "provider_abstraction_standard_v1"

DOMAIN_LIST: Tuple[str, ...] = (
    "OCR",
    "Vision",
    "Voice ASR",
    "Voice TTS",
    "Map",
    "Library",
    "Hive",
    "Memory",
)

CONSISTENCY_FIELDS: Tuple[str, ...] = (
    "provider_domain",
    "runtime_type",
    "provider_candidate_id",
    "provider_readiness_status",
    "provider_selection_status",
    "provider_invocation_status",
    "provider_output_contract",
    "adapter_ref",
    "failure_route",
    "fallback_candidate",
    "evidence_refs",
    "boundary_status",
    "source_chain",
    "version_ref",
)

BOUNDARY_MATRIX_FALSE: Tuple[str, ...] = (
    "historical_verdict_rewritten_now",
    "historical_file_deleted_now",
    "provider_runtime_enabled_now",
    "provider_selected_now",
    "provider_invoked_now",
    "provider_imported_now",
    "provider_auto_switch_executed_now",
    "runtime_core_rewritten_now",
    "adapter_runtime_enabled_now",
    "model_runtime_invoked_now",
    "qianwen_tts_invoked_now",
    "paddleocr_invoked_now",
    "rapidocr_invoked_now",
    "external_provider_invoked_now",
    "map_provider_invoked_now",
    "memory_written_now",
    "world_model_written_now",
    "task_state_committed_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Provider Abstraction Planning GO ≠ provider abstraction applied",
    "provider candidate contract planned ≠ provider selected",
    "legacy absorption planned ≠ historical files modified",
    "Qianwen candidate remains not selected/invoked",
    "Display Gate deferred remains not skipped",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/provider_abstraction_standard_alignment_planning"
)


def _meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "current_preferred_provider_candidate": CURRENT_PREFERRED_PROVIDER_CANDIDATE,
        "four_layer_architecture": FOUR_LAYER_ARCHITECTURE,
        "provider_abstraction_standard_alignment_planning_only": True,
    }
    for f in BOUNDARY_MATRIX_FALSE:
        meta[f] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_provider_abstraction_standard_alignment_planning_v1(
    *,
    midplatform_post_output_chain_simulation_roadmap_decision_root: str,
    midplatform_tts_runtime_dryrun_and_review_root: str,
    midplatform_tts_runtime_planning_root: str,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: str,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: str,
    model_registry_canonicalization_post_dryrun_review_root: str,
    midplatform_module_definition_template_planning_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    roadmap_root = Path(midplatform_post_output_chain_simulation_roadmap_decision_root).expanduser().resolve()
    tts_dr_root = Path(midplatform_tts_runtime_dryrun_and_review_root).expanduser().resolve()
    tts_plan_root = Path(midplatform_tts_runtime_planning_root).expanduser().resolve()
    ocr_auth_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
    ).expanduser().resolve()
    harness_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
    ).expanduser().resolve()
    registry_root = Path(model_registry_canonicalization_post_dryrun_review_root).expanduser().resolve()
    template_root = Path(midplatform_module_definition_template_planning_root).expanduser().resolve()

    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    tts_dr_sm = _try_read_json(tts_dr_root / "summary.json") or {}
    tts_provider_register = _try_read_json(tts_plan_root / "current_tts_provider_candidate_register_v1.json") or {}
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}
    harness_registry = _try_read_json(
        harness_root / "controlled_provider_harness_registry_entry_review_v1.json"
    ) or {}
    ocr_auth_vr = _try_read_json(ocr_auth_root / "verifier_report.json") or {}
    registry_vr = _try_read_json(registry_root / "verifier_report.json") or {}
    template_vr = _try_read_json(template_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_meta(),
        "upstream_post_output_chain_roadmap_root": str(roadmap_root),
        "upstream_tts_runtime_dryrun_root": str(tts_dr_root),
        "upstream_tts_runtime_planning_root": str(tts_plan_root),
        "upstream_ocr_real_dependency_authorization_dryrun_root": str(ocr_auth_root),
        "upstream_harness_post_review_root": str(harness_root),
        "upstream_model_registry_post_review_root": str(registry_root),
        "upstream_template_planning_root": str(template_root),
        "output_root": str(out_root),
        "display_gate_deferred_not_skipped": True,
    }

    if roadmap_vr.get("verifier") != "GO":
        blockers.append("Post Output Chain Simulation Roadmap Decision verifier must be GO")
    if roadmap_sm.get("final_decision") != UPSTREAM_ROADMAP_FINAL_GO:
        blockers.append("roadmap final_decision mismatch")
    if roadmap_sm.get("selected_route") != ROUTE_A_LABEL:
        blockers.append("selected_route must be Route A — Provider Abstraction Standard Alignment")

    if tts_dr_sm.get("qianwen_tts_invoked_now") is not False:
        blockers.append("qianwen_tts_candidate must not be invoked")
    if tts_dr_sm.get("current_preferred_provider_candidate") != CURRENT_PREFERRED_PROVIDER_CANDIDATE:
        blockers.append("current_preferred_provider_candidate mismatch")

    qianwen_registered = any(
        x.get("provider_candidate_id") == CURRENT_PREFERRED_PROVIDER_CANDIDATE
        for x in (tts_provider_register.get("provider_candidates") or [])
    )
    if not qianwen_registered:
        blockers.append("qianwen_tts_candidate must be registered in current_tts_provider_candidate_register")

    if harness_vr.get("verifier") != "GO":
        blockers.append("ControlledProviderReadinessHarness post-review must be GO")
    if harness_registry.get("review_pass") is not True:
        blockers.append("ControlledProviderReadinessHarness registry entry review must pass")

    if ocr_auth_vr.get("verifier") != "GO":
        blockers.append("OCR real dependency authorization dryrun+review must be GO")
    if registry_vr.get("verifier") != "GO":
        blockers.append("Model registry canonicalization post dryrun review must be GO")
    if template_vr.get("verifier") != "GO":
        blockers.append("Module definition template planning must be GO")

    input_ok = len(blockers) == 0

    policy = {
        "policy_id": "provider_abstraction_standard_alignment_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "planning_only": True,
        "no_historical_verdict_rewrite": True,
        "no_provider_invocation": True,
        "standard_id": STANDARD_ID,
        **meta,
    }

    input_review = {
        "review_id": "post_output_chain_roadmap_input_review_v1",
        "roadmap_verifier": roadmap_vr.get("verifier"),
        "selected_route": roadmap_sm.get("selected_route"),
        "roadmap_final_decision": roadmap_sm.get("final_decision"),
        "tts_runtime_corrected_abstract_runtime": True,
        "qianwen_registered_not_invoked": qianwen_registered and (tts_dr_sm.get("qianwen_tts_invoked_now") is False),
        "harness_post_review_go": harness_vr.get("verifier") == "GO",
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    standard = {
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
        "unified_principles": [
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
        ],
        **meta,
    }

    provider_candidate_contract = {
        "contract_id": "provider_candidate_contract_v1",
        "required_fields": [
            "provider_candidate_id",
            "provider_domain",
            "provider_type",
            "runtime_family",
            "adapter_ref",
            "capability_tags",
            "input_contract_ref",
            "output_contract_ref",
            "readiness_status",
            "selection_status",
            "invocation_status",
            "authorization_refs",
            "evidence_refs",
            "failure_route_refs",
            "fallback_candidate_refs",
            "boundary_status",
            "provider_specific_config_ref",
            "candidate_only",
            "selected_for_execution",
            "invoked_now",
        ],
        "defaults": {"candidate_only": True, "selected_for_execution": False, "invoked_now": False},
        **meta,
    }

    adapter_boundary = {
        "contract_id": "provider_adapter_boundary_contract_v1",
        "rules": [
            "provider adapter may contain provider-specific logic",
            "runtime core must not contain provider-specific logic",
            "adapter change must not rewrite runtime core",
            "adapter output must follow domain output contract",
            "adapter cannot bypass readiness / authorization",
            "adapter cannot write Memory / WorldModel directly",
            "adapter cannot emit user output directly",
        ],
        **meta,
    }

    readiness_binding = {
        "contract_id": "provider_readiness_binding_contract_v1",
        "rules": [
            "ControlledProviderReadinessHarness required for provider readiness",
            "readiness applies to provider_candidate, not runtime core",
            "readiness evidence must be preserved",
            "readiness pass ≠ selected provider",
            "readiness fail → hold / issue_trace / fallback candidate",
            "readiness unknown → request readiness validation",
        ],
        "controlled_provider_readiness_harness_ref": "controlled_provider_readiness_harness_v1",
        **meta,
    }

    selection_authz = {
        "policy_id": "provider_selection_authorization_policy_v1",
        "rules": [
            "provider selection requires explicit authorization",
            "provider selection cannot happen during planning/dryrun",
            "provider selection must cite readiness evidence",
            "provider selection must cite execution window later",
            "selected provider still does not mean invoked provider",
            "provider invocation requires separate runtime authorization",
        ],
        **meta,
    }

    switch_policy = {
        "policy_id": "provider_switch_policy_v1",
        "rules": [
            "no automatic switch on provider failure",
            "switch requires policy + readiness + authorization",
            "switch preserves source_chain",
            "switch must not rewrite runtime core",
            "switch must not hide failure",
            "fallback_candidate is candidate only",
            "provider_auto_switch_executed_now=false",
        ],
        "provider_auto_switch_executed_now": False,
        **meta,
    }

    alignment_matrix = {
        "matrix_id": "domain_provider_alignment_matrix_v1",
        "domains": list(DOMAIN_LIST),
        "domain_count": len(DOMAIN_LIST),
        "standard_id": STANDARD_ID,
        "runtime_core_abstract_for_all_domains": True,
        **meta,
    }

    ocr_plan = {
        "plan_id": "ocr_provider_alignment_plan_v1",
        "confirmations": [
            "OCR Runtime / OCR Capability ≠ PaddleOCR / RapidOCR / external OCR",
            "PaddleOCR / RapidOCR / external OCR = ocr_provider_candidate",
            "historical PaddleOCR / RapidOCR refs remain read_only_evidence_source",
            "future OCR phases must use provider_abstraction_standard_v1",
            "OCR provider invocation still requires authorization / execution window",
        ],
        **meta,
    }
    vision_plan = {
        "plan_id": "vision_provider_alignment_plan_v1",
        "confirmations": [
            "Vision Runtime / Vision Capability ≠ YOLO / Grounded SAM / VLM provider",
            "YOLO / Grounded SAM / VLM / local model / cloud model = vision_provider_candidate",
            "tracker / detector / segmenter adapters are provider adapters",
            "provider output remains candidate/evidence, not fact/user output",
        ],
        **meta,
    }
    voice_asr_plan = {
        "plan_id": "voice_asr_provider_alignment_plan_v1",
        "confirmations": [
            "ASR Runtime ≠ Qwen-ASR / SenseVoice / Whisper / VibeVoice / pyannote",
            "ASR providers are voice_asr_provider_candidate",
            "speaker diarization / voiceprint providers also follow provider candidate contract",
            "voice identity binding requires separate privacy / consent / memory policy",
        ],
        **meta,
    }
    voice_tts_plan = {
        "plan_id": "voice_tts_provider_alignment_plan_v1",
        "confirmations": [
            "TTS Runtime ≠ Qianwen / MOSS-TTS / local TTS / system TTS",
            "qianwen_tts_candidate is current_preferred_provider_candidate",
            "qianwen_tts_candidate ≠ selected_provider ≠ invoked_provider",
            "future TTS providers use same provider candidate contract",
        ],
        **meta,
    }
    map_plan = {
        "plan_id": "map_provider_alignment_plan_v1",
        "confirmations": [
            "Map Context / Navigation Context ≠ 高德 / Apple Maps / Google Maps / offline map",
            "map SDKs are map_provider_candidate",
            "map provider output remains context/evidence/candidate",
            "navigation action requires separate decision/action policy",
        ],
        **meta,
    }
    lhm_plan = {
        "plan_id": "library_hive_memory_provider_alignment_plan_v1",
        "confirmations": [
            "Library provider / Hive provider / Memory storage provider may have provider candidates",
            "storage / retrieval / indexing providers must not be treated as Memory/Library/Hive core",
            "provider output is retrieval/evidence candidate unless fact/write policy admits it",
            "memory write requires separate admission policy",
        ],
        **meta,
    }

    legacy_absorption = {
        "plan_id": "legacy_provider_reference_absorption_plan_v1",
        "markers": {
            "legacy_provider_specific_reference": True,
            "absorbed_by": STANDARD_ID,
            "read_only_evidence_source": True,
            "physical_rewrite_required": False,
            "historical_verdict_preserved": True,
            "future_new_phase_must_use_provider_abstraction": True,
        },
        "coverage": [
            "OCR PaddleOCR/RapidOCR historical refs",
            "TTS Qianwen current candidate refs",
            "Vision provider/tool refs where present",
            "ASR provider refs where present",
            "Map SDK/provider refs where present",
        ],
        **meta,
    }

    consistency_rule_matrix = {
        "matrix_id": "provider_abstraction_consistency_rule_matrix_v1",
        "fields": list(CONSISTENCY_FIELDS),
        "field_count": len(CONSISTENCY_FIELDS),
        "applies_to_domains": list(DOMAIN_LIST),
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "provider_abstraction_boundary_matrix_v1",
        "all_false": True,
        "matrix": {k: False for k in BOUNDARY_MATRIX_FALSE},
        **meta,
    }

    dryrun_plan = {
        "plan_id": "provider_abstraction_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate provider_abstraction_standard_candidate",
            "generate domain_provider_alignment_matrix_candidate",
            "generate provider_candidate_contract sample",
            "generate legacy absorption markers",
            "verify OCR/Vision/ASR/TTS/Map/Library/Hive/Memory alignment",
            "verify no historical verdict rewrite, no provider invocation, no runtime core rewrite",
        ],
        **meta,
    }

    non_claims = {"register_id": "non_claims_register_v1", "non_claims": list(NON_CLAIMS), **meta}

    planning_pass = input_ok
    decision = {
        "decision_id": "provider_abstraction_standard_alignment_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        "standard_id": STANDARD_ID,
        "selected_route": ROUTE_A_LABEL,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": planning_pass,
        "violations": list(blockers),
        "planning_pass": planning_pass,
        "final_decision": decision["final_decision"],
        "recommended_next_phase": decision["recommended_next_phase"],
        "selected_route": ROUTE_A_LABEL,
        **meta,
    }

    return {
        "provider_abstraction_standard_alignment_policy": policy,
        "post_output_chain_roadmap_input_review": input_review,
        "provider_abstraction_standard": standard,
        "provider_candidate_contract": provider_candidate_contract,
        "provider_adapter_boundary_contract": adapter_boundary,
        "provider_readiness_binding_contract": readiness_binding,
        "provider_selection_authorization_policy": selection_authz,
        "provider_switch_policy": switch_policy,
        "domain_provider_alignment_matrix": alignment_matrix,
        "ocr_provider_alignment_plan": ocr_plan,
        "vision_provider_alignment_plan": vision_plan,
        "voice_asr_provider_alignment_plan": voice_asr_plan,
        "voice_tts_provider_alignment_plan": voice_tts_plan,
        "map_provider_alignment_plan": map_plan,
        "library_hive_memory_provider_alignment_plan": lhm_plan,
        "legacy_provider_reference_absorption_plan": legacy_absorption,
        "provider_abstraction_consistency_rule_matrix": consistency_rule_matrix,
        "provider_abstraction_boundary_matrix": boundary_matrix,
        "provider_abstraction_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "provider_abstraction_standard_alignment_planning_decision": decision,
        "summary": summary,
    }
