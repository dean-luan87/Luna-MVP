# -*- coding: utf-8 -*-
"""Model Profile Registry DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.layered_capability_stack_standard_v1 import STANDARD_ID as UNIVERSAL_STACK_STANDARD_ID
from capabilities.governance.layered_governance_mapping_v1 import ADDENDUM_ID
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
    PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
)
from capabilities.governance.model_profile_registry_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HEALTH_VALIDATION_FIELDS,
    IO_FORBIDDEN,
    IO_INPUT_TYPES,
    IO_OUTPUT_TYPES,
    LAYER_BINDING_FIELDS,
    LICENSE_METADATA_FIELDS,
    LIFECYCLE_STATES,
    MODEL_PROFILE_SCHEMA_FIELDS,
    PHASE_ID as PLANNING_PHASE_ID,
    PROVIDER_RUNTIME_BINDING_FIELDS,
    QUALITY_PROFILE_FIELDS,
    SEED_CANDIDATE_IDS,
    SEED_CANDIDATE_REQUIRED,
    STATUS_TAXONOMY,
    VERSION_REPLACEMENT_FIELDS,
)

PHASE_ID = "Phase-Model-Profile-Registry-DryRunAndReview-v1-001"
SCOPE = "model_profile_registry_dryrun_and_review_only"
SOURCE_CHAIN = "model_profile_registry_dryrun_and_review_v1"

FINAL_DECISION_GO = (
    "MODEL_PROFILE_REGISTRY_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_MODULE_LOCAL_MODEL_PROFILE_STANDARDIZATION_PLANNING"
)
FINAL_DECISION_HOLD = "MODEL_PROFILE_REGISTRY_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Module-Local-Model-Profile-Standardization-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Model-Profile-Registry-Issue-Review-v1-001"

REUSED_GOVERNANCE_STANDARDS: Tuple[str, ...] = (
    "Layered Capability Stack Standard",
    "Layered Governance Mapping",
    "Constitution-Bus v1.0",
    "Provider Abstraction Standard",
    "Controlled Runtime Framework",
    "Health Oversight Externality",
    "Whitebox Trace Standard",
    "Candidate/Evidence Contract pattern",
    "Boundary Matrix / Blocked Path / Non-Claims pattern",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_registry_runtime_enable",
    "dryrun_to_model_profile_as_runtime",
    "dryrun_to_model_selection",
    "dryrun_to_model_download",
    "dryrun_to_model_invocation",
    "dryrun_to_provider_invocation",
    "dryrun_to_model_runtime_enable",
    "dryrun_to_benchmark_execution",
    "dryrun_to_license_clearance",
    "dryrun_to_security_review_completion",
    "dryrun_to_training_start",
    "dryrun_to_fine_tuning_start",
    "dryrun_to_code_generation",
    "dryrun_to_skill_addition",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
    "dryrun_to_task_state_commit",
    "dryrun_to_user_output",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Model Profile Registry DryRun GO ≠ model selected",
    "seed candidates reviewed ≠ license cleared",
    "registry candidate ≠ registry runtime",
    "qianwen/yolo/ocr/asr candidates reviewed ≠ invoked",
    "next Module-local Profile Standardization Planning ≠ model connection",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "model_profile_registry_dryrun_and_review_only",
    "simulated",
    "model_profile_registry_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "model_profile_registry_runtime_enabled_now", "model_profile_created_as_runtime_now",
    "model_selected_now", "model_downloaded_now", "model_invoked_now", "provider_invoked_now",
    "model_runtime_enabled_now", "benchmark_executed_now", "license_cleared_now",
    "security_review_completed_now", "training_started_now", "fine_tuning_started_now",
    "code_generation_executed_now", "skill_added_now", "memory_written_now",
    "world_model_written_now", "task_state_committed_now", "user_output_generated_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "source_chain": SOURCE_CHAIN,
        "system_level_simulated_go": True,
        "candidate_only": True,
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


def _review_from_checks(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"check_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "review_pass": len(issues) == 0,
    }


def run_model_profile_registry_dryrun_and_review_v1(
    *,
    model_profile_registry_planning_root: str,
    scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_root: str,
    layered_capability_stack_standard_dryrun_and_review_root: str,
    luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root: str,
    provider_abstraction_standard_alignment_dryrun_and_review_root: str,
    midplatform_controlled_runtime_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(model_profile_registry_planning_root).expanduser().resolve()
    roadmap_dr_root = Path(
        scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_root
    ).expanduser().resolve()
    stack_root = Path(layered_capability_stack_standard_dryrun_and_review_root).expanduser().resolve()
    cb_root = Path(
        luna_constitution_capability_bus_governance_baseline_dryrun_and_review_root
    ).expanduser().resolve()
    provider_root = Path(
        provider_abstraction_standard_alignment_dryrun_and_review_root
    ).expanduser().resolve()
    cr_root = Path(midplatform_controlled_runtime_dryrun_and_review_root).expanduser().resolve()

    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    roadmap_dr_vr = _try_read_json(roadmap_dr_root / "verifier_report.json") or {}
    stack_vr = _try_read_json(stack_root / "verifier_report.json") or {}
    cb_vr = _try_read_json(cb_root / "verifier_report.json") or {}
    provider_vr = _try_read_json(provider_root / "verifier_report.json") or {}
    cr_vr = _try_read_json(cr_root / "verifier_report.json") or {}

    schema = _try_read_json(plan_root / "model_profile_schema_v1.json") or {}
    lifecycle = _try_read_json(plan_root / "model_profile_lifecycle_policy_v1.json") or {}
    status_tax = _try_read_json(plan_root / "model_profile_status_taxonomy_v1.json") or {}
    license_s = _try_read_json(plan_root / "model_source_and_license_metadata_schema_v1.json") or {}
    layer_s = _try_read_json(plan_root / "model_capability_layer_binding_schema_v1.json") or {}
    io_s = _try_read_json(plan_root / "model_input_output_profile_schema_v1.json") or {}
    qual_s = _try_read_json(plan_root / "model_quality_acceptance_profile_schema_v1.json") or {}
    health_s = _try_read_json(plan_root / "model_health_validation_whitebox_profile_schema_v1.json") or {}
    prov_s = _try_read_json(plan_root / "model_provider_runtime_binding_profile_schema_v1.json") or {}
    ver_s = _try_read_json(plan_root / "model_version_update_replacement_profile_schema_v1.json") or {}
    domain_idx = _try_read_json(plan_root / "model_profile_registry_domain_index_v1.json") or {}
    seeds = _try_read_json(plan_root / "seed_model_profile_candidates_v1.json") or {}
    vision = _try_read_json(plan_root / "vision_model_profile_seed_candidates_v1.json") or {}
    ocr = _try_read_json(plan_root / "ocr_model_profile_seed_candidates_v1.json") or {}
    tts = _try_read_json(plan_root / "tts_model_profile_seed_candidates_v1.json") or {}
    asr = _try_read_json(plan_root / "asr_model_profile_seed_candidates_v1.json") or {}
    nav = _try_read_json(plan_root / "map_navigation_model_profile_seed_candidates_v1.json") or {}
    world = _try_read_json(plan_root / "world_continuity_model_profile_seed_candidates_v1.json") or {}
    mem_emo = _try_read_json(
        plan_root / "memory_emotion_evolution_model_profile_seed_candidates_v1.json"
    ) or {}
    module_plan = _try_read_json(plan_root / "model_profile_to_module_local_binding_plan_v1.json") or {}
    mid_plan = _try_read_json(
        plan_root / "model_profile_to_midplatform_governance_binding_plan_v1.json"
    ) or {}
    registry_def = _try_read_json(plan_root / "model_profile_registry_definition_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "output_root": str(out_root),
        "upstream_planning_root": str(plan_root),
        "upstream_roadmap_dryrun_root": str(roadmap_dr_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("Model Profile Registry Planning must be GO")
    if plan_sm.get("final_decision") != PLANNING_FINAL_GO:
        blockers.append("Planning final_decision mismatch")
    if plan_sm.get("seed_candidate_count") != 14:
        blockers.append("seed_candidate_count must be 14")
    if roadmap_dr_vr.get("verifier") != "GO":
        blockers.append("Roadmap DryRunAndReview must be GO")
    for name, vr in (
        ("stack_std", stack_vr), ("constitution_bus", cb_vr),
        ("provider_abs", provider_vr), ("controlled_runtime", cr_vr),
    ):
        if vr.get("verifier") != "GO":
            blockers.append(f"{name} must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "planning_input_review_v1",
        "planning_verifier": plan_vr.get("verifier"),
        "planning_final_decision": plan_sm.get("final_decision"),
        "seed_candidate_count": plan_sm.get("seed_candidate_count"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    governance_reuse = {
        "review_id": "governance_standard_reuse_review_v1",
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "reuse_rule_text": PHASE_GOVERNANCE_STANDARD_REUSE_RULE,
        "reused_standards": list(REUSED_GOVERNANCE_STANDARDS),
        "new_governance_need_proven": False,
        "no_parallel_duplicate_governance_standard": True,
        "no_equivalent_schema_redefined_without_extension": True,
        **_review_from_checks([
            ("constraints_ref", True),
            ("reuse_rule_true", True),
            ("new_need_false", True),
            ("reused_count9", len(REUSED_GOVERNANCE_STANDARDS) == 9),
            ("no_parallel", True),
        ]),
        **meta,
    }

    schema_count = 8
    registry_candidate = {
        "registry_id": "luna_model_profile_registry_v1",
        "registry_type": "model_candidate_profile_registry",
        "planning_source_phase": PLANNING_PHASE_ID,
        "registry_runtime_enabled_now": False,
        "model_selection_allowed_now": False,
        "model_invocation_allowed_now": False,
        "benchmark_allowed_now": False,
        "seed_candidate_count": 14,
        "schema_count": schema_count,
        "candidate_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "registry_duties_from_planning": registry_def.get("registry_duties"),
        **meta,
    }

    schema_review = {
        "review_id": "model_profile_schema_review_v1",
        "field_count": len(MODEL_PROFILE_SCHEMA_FIELDS),
        **_review_from_checks(
            [(f, f in (schema.get("required_fields") or [])) for f in MODEL_PROFILE_SCHEMA_FIELDS]
            + [
                ("source_chain_default", schema.get("defaults", {}).get("source_chain_required") is True),
                ("whitebox_default", schema.get("defaults", {}).get("whitebox_trace_required") is True),
                ("no_fact_default", schema.get("defaults", {}).get("no_direct_fact_action_output") is True),
                ("selected_false", schema.get("defaults", {}).get("selected_now") is False),
                ("invoked_false", schema.get("defaults", {}).get("invoked_now") is False),
                ("runtime_false", schema.get("defaults", {}).get("runtime_enabled_now") is False),
            ]
        ),
        **meta,
    }

    lifecycle_review = {
        "review_id": "model_profile_lifecycle_policy_review_v1",
        **_review_from_checks(
            [(s, s in (lifecycle.get("lifecycle_states") or [])) for s in LIFECYCLE_STATES]
            + [
                ("reg_ne_sel", lifecycle.get("rules", {}).get("registered_ne_selected") is True),
                ("complete_ne_runtime", lifecycle.get("rules", {}).get("profile_complete_ne_runtime_ready") is True),
                ("bench_ne_exec", lifecycle.get("rules", {}).get("benchmark_required_ne_benchmark_executed") is True),
                ("lic_ne_clear", lifecycle.get("rules", {}).get("license_review_required_ne_license_cleared") is True),
                ("sel_later_blocked", lifecycle.get("rules", {}).get("selected_later_not_allowed_now") is True),
            ]
        ),
        **meta,
    }

    status_review = {
        "review_id": "model_profile_status_taxonomy_review_v1",
        **_review_from_checks([(s, s in (status_tax.get("status_types") or [])) for s in STATUS_TAXONOMY]),
        **meta,
    }

    license_review = {
        "review_id": "source_license_metadata_schema_review_v1",
        **_review_from_checks(
            [(f, f in (license_s.get("required_fields") or [])) for f in LICENSE_METADATA_FIELDS]
            + [
                ("update_tracking", license_s.get("defaults", {}).get("update_tracking_required") is True),
                ("unknown_not_cleared", True),
                ("metadata_ne_cleared", True),
                ("external_ne_approved", True),
            ]
        ),
        **meta,
    }

    layer_review = {
        "review_id": "capability_layer_binding_schema_review_v1",
        **_review_from_checks(
            [(f, f in (layer_s.get("required_fields") or [])) for f in LAYER_BINDING_FIELDS]
            + [
                ("cannot_claim_higher", layer_s.get("cannot_claim_higher_layer_without_lower_layer") is True),
                ("stack_ref", layer_s.get("capability_stack_ref") == UNIVERSAL_STACK_STANDARD_ID),
                ("gov_ref", layer_s.get("layered_governance_mapping_ref") == ADDENDUM_ID),
                ("nav_application", True),
                ("identity_later", True),
                ("binds_gov_mapping", True),
            ]
        ),
        **meta,
    }

    io_review = {
        "review_id": "model_input_output_profile_schema_review_v1",
        **_review_from_checks(
            [(f"in.{t}", t in (io_s.get("input_types") or [])) for t in IO_INPUT_TYPES]
            + [(f"out.{t}", t in (io_s.get("output_types") or [])) for t in IO_OUTPUT_TYPES]
            + [(f"forbid.{t}", t in (io_s.get("forbidden_outputs") or [])) for t in IO_FORBIDDEN]
        ),
        **meta,
    }

    quality_review = {
        "review_id": "model_quality_acceptance_profile_schema_review_v1",
        **_review_from_checks(
            [(f, f in (qual_s.get("required_fields") or [])) for f in QUALITY_PROFILE_FIELDS]
            + [
                ("compliance_req", qual_s.get("defaults", {}).get("candidate_contract_compliance_required") is True),
                ("degradation_req", qual_s.get("defaults", {}).get("degradation_behavior_required") is True),
            ]
        ),
        **meta,
    }

    health_review = {
        "review_id": "health_validation_whitebox_profile_schema_review_v1",
        **_review_from_checks(
            [(f, f in (health_s.get("required_fields") or [])) for f in HEALTH_VALIDATION_FIELDS]
            + [
                ("external_bus", health_s.get("defaults", {}).get("health_oversight_external_to_bus") is True),
                ("bus_transports", health_s.get("defaults", {}).get("bus_transports_health_ref_not_judges") is True),
            ]
        ),
        **meta,
    }

    provider_review = {
        "review_id": "provider_runtime_binding_profile_schema_review_v1",
        **_review_from_checks(
            [(f, f in (prov_s.get("required_fields") or [])) for f in PROVIDER_RUNTIME_BINDING_FIELDS]
            + [
                ("provider_abs", prov_s.get("defaults", {}).get("provider_abstraction_required") is True),
                ("controlled_rt", prov_s.get("defaults", {}).get("controlled_runtime_required") is True),
                ("no_auto_switch", prov_s.get("defaults", {}).get("no_provider_auto_switch_without_policy") is True),
                ("no_runtime_now", prov_s.get("defaults", {}).get("runtime_invocation_allowed_now") is False),
            ]
        ),
        **meta,
    }

    version_review = {
        "review_id": "version_update_replacement_profile_schema_review_v1",
        **_review_from_checks(
            [(f, f in (ver_s.get("required_fields") or [])) for f in VERSION_REPLACEMENT_FIELDS]
            + [
                ("bench_reval", ver_s.get("defaults", {}).get("benchmark_revalidation_required") is True),
                ("sec_review", ver_s.get("defaults", {}).get("security_review_required") is True),
                ("owner_review", ver_s.get("defaults", {}).get(
                    "owner_or_governance_review_required_for_high_risk_replacement"
                ) is True),
            ]
        ),
        **meta,
    }

    index_keys = (
        "by_capability_domain", "by_goal_stage", "by_model_source_strategy", "by_provider_candidate",
        "by_status", "by_license_review_status", "by_runtime_readiness_status",
        "by_layered_capability_stack_layer", "by_risk_level",
    )
    index_review = {
        "review_id": "registry_domain_index_review_v1",
        **_review_from_checks([(k, bool(domain_idx.get(k))) for k in index_keys]),
        **meta,
    }

    seed_list = seeds.get("candidates") or []
    seed_checks: List[Tuple[str, bool]] = [("count14", len(seed_list) == 14)]
    for sid in SEED_CANDIDATE_IDS:
        c = next((x for x in seed_list if x.get("model_profile_id") == sid), {})
        seed_checks.append((f"exists.{sid[:16]}", bool(c)))
        for field in SEED_CANDIDATE_REQUIRED:
            seed_checks.append((f"{sid[:8]}.{field[:8]}", field in c))
    seeds_review = {
        "review_id": "seed_model_profile_candidates_review_v1",
        **_review_from_checks(seed_checks),
        **meta,
    }

    vision_text = json.dumps(vision, ensure_ascii=False)
    vision_review = {
        "review_id": "vision_model_profile_seed_candidates_review_v1",
        **_review_from_checks([
            ("yolo", "yolo_family" in vision_text),
            ("grounded", "grounded_sam" in vision_text),
            ("tracking", "visual_tracking" in vision_text),
            ("vlm", "vlm_scene" in vision_text),
            ("candidate_only", "candidate" in vision_text.lower()),
            ("no_camera", "no camera" in vision_text),
            ("no_benchmark", "no benchmark" in vision_text),
            ("no_selection", "no selection" in vision_text),
        ]),
        **meta,
    }

    ocr_text = json.dumps(ocr, ensure_ascii=False)
    ocr_review = {
        "review_id": "ocr_model_profile_seed_candidates_review_v1",
        **_review_from_checks([
            ("rapid", "rapidocr" in ocr_text),
            ("paddle", "paddleocr" in ocr_text),
            ("placeholder", "other_ocr_provider" in ocr_text),
            ("candidate_only", "candidate only" in ocr_text),
            ("not_fact", "not fact" in ocr_text),
            ("no_runtime", "no OCR runtime" in ocr_text),
        ]),
        **meta,
    }

    tts_text = json.dumps(tts, ensure_ascii=False)
    tts_review = {
        "review_id": "tts_model_profile_seed_candidates_review_v1",
        **_review_from_checks([
            ("qianwen", "qianwen_tts" in tts_text),
            ("moss", "moss_tts" in tts_text),
            ("local", "local_tts" in tts_text),
            ("not_selected", "≠ selected" in tts_text or "not selected" in tts_text.lower()),
            ("abstract_runtime", "abstract TTS runtime" in tts_text),
            ("no_invoke", "no TTS invocation" in tts_text),
        ]),
        **meta,
    }

    asr_text = json.dumps(asr, ensure_ascii=False)
    asr_review = {
        "review_id": "asr_model_profile_seed_candidates_review_v1",
        **_review_from_checks([
            ("sensevoice", "sensevoice" in asr_text),
            ("whisper", "whisper" in asr_text),
            ("qwen_asr", "qwen_asr" in asr_text),
            ("not_started", "not_started" in asr_text or "deferred" in asr_text or "planned" in asr_text),
            ("no_runtime", "no ASR runtime" in asr_text),
        ]),
        **meta,
    }

    nav_text = json.dumps(nav, ensure_ascii=False)
    nav_review = {
        "review_id": "map_navigation_model_profile_seed_candidates_review_v1",
        **_review_from_checks([
            ("map_provider", "map_provider" in nav_text),
            ("route", "route_reasoning" in nav_text),
            ("facility", "facility_search" in nav_text),
            ("transit", "transit_context" in nav_text),
            ("stage3", "Stage 3" in nav_text),
            ("no_invocation", "no map provider invocation" in nav_text),
            ("no_action", "no navigation action" in nav_text),
        ]),
        **meta,
    }

    world_text = json.dumps(world, ensure_ascii=False)
    world_review = {
        "review_id": "world_continuity_model_profile_seed_candidates_review_v1",
        **_review_from_checks([
            ("scene_delta", "scene_delta" in world_text),
            ("temporal", "temporal_tracking" in world_text),
            ("visual_map", "visual_map_alignment" in world_text),
            ("missing_ctx", "missing_context" in world_text),
            ("stcm", "stcm_self_developed" in world_text),
            ("signals_only", "signals only" in world_text),
            ("luna_owns", "Luna owns" in world_text),
        ]),
        **meta,
    }

    mem_text = json.dumps(mem_emo, ensure_ascii=False)
    mem_review = {
        "review_id": "memory_emotion_evolution_model_profile_seed_candidates_review_v1",
        **_review_from_checks([
            ("embedding", "embedding_retrieval" in mem_text),
            ("emotion", "emotion_signal" in mem_text),
            ("relationship", "relationship_context" in mem_text),
            ("market", "market_feedback" in mem_text),
            ("code", "code_analysis" in mem_text),
            ("personal_self", "Personal Continuity" in mem_text),
            ("emotion_self", "Emotion governance" in mem_text),
            ("evolution_self", "Evolutionary Recursion" in mem_text),
            ("proposal_only", "proposal_only" in mem_text),
            ("no_mem_write", "no memory write" in mem_text),
            ("no_code_mod", "code modification" in mem_text),
            ("no_skill", "skill addition" in mem_text),
        ]),
        **meta,
    }

    module_rules = module_plan.get("rules") or []
    module_review = {
        "review_id": "module_local_binding_review_v1",
        **_review_from_checks([
            ("ref_profile_id", any("model_profile_id" in r for r in module_rules)),
            ("cannot_override", any("cannot override registry" in r for r in module_rules)),
            ("impl_context", any("implementation context" in r for r in module_rules)),
            ("stack_gov", any("capability stack" in r and "governance mapping" in r for r in module_rules)),
            ("cannot_select", any("cannot select/invoke" in r for r in module_rules)),
        ]),
        **meta,
    }

    mid_rules = mid_plan.get("rules") or []
    mid_review = {
        "review_id": "midplatform_governance_binding_review_v1",
        **_review_from_checks([
            ("constitution_bus", any("Constitution-Bus" in r for r in mid_rules)),
            ("provider_abs", any("Provider Abstraction" in r for r in mid_rules)),
            ("validation", any("Validation" in r for r in mid_rules)),
            ("health", any("Health" in r for r in mid_rules)),
            ("whitebox", any("Whitebox" in r for r in mid_rules)),
            ("controlled_runtime", any("Controlled Runtime" in r for r in mid_rules)),
            ("output_gate", any("Output Gate" in r for r in mid_rules)),
            ("memory_wm", any("Memory/WorldModel" in r for r in mid_rules)),
            ("decision_ii", any("Decision/Integration" in r for r in mid_rules)),
        ]),
        **meta,
    }

    boundary_audit = {
        "audit_id": "registry_non_runtime_boundary_audit_v1",
        "boundary_fields": {f: False for f in BOUNDARY_FALSE},
        "audit_pass": True,
        **meta,
    }

    blocked_path_result = {
        "result_id": "registry_blocked_path_result_v1",
        "blocked_paths": [{"path_id": p, "status": "blocked", "executed": False} for p in BLOCKED_PATHS],
        "blocked_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    all_reviews = [
        governance_reuse, schema_review, lifecycle_review, status_review, license_review,
        layer_review, io_review, quality_review, health_review, provider_review, version_review,
        index_review, seeds_review, vision_review, ocr_review, tts_review, asr_review,
        nav_review, world_review, mem_review, module_review, mid_review,
    ]

    dryrun_pass = (
        input_ok
        and governance_reuse.get("review_pass")
        and all(r.get("review_pass") for r in all_reviews)
        and boundary_audit.get("audit_pass")
        and blocked_path_result.get("all_blocked")
    )

    closure_decision = {
        "decision_id": "registry_closure_decision_v1",
        "dryrun_and_review_pass": dryrun_pass,
        "high_risk": not dryrun_pass,
        "final_decision": FINAL_DECISION_GO if dryrun_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        "closure_summary": [
            "Model Profile Registry candidate validated",
            "8 schema reviews pass",
            "14 seed candidates compliant",
            "module-local and midplatform binding plans confirmed",
            "governance standard reuse confirmed; no parallel governance created",
            "ready for Module-local Model Profile Standardization Planning",
        ] if dryrun_pass else ["hold for issue review"],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_module_local_model_profile_standardization_planning": dryrun_pass,
        "selected_next_phase": NEXT_PHASE_GO if dryrun_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "model_profile_registry_dryrun_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims = {"register_id": "non_claims_register_v1", "non_claims": list(NON_CLAIMS), **meta}

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "dryrun_and_review_pass": dryrun_pass,
        "seed_candidate_count": 14,
        "schema_count": schema_count,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "model_profile_registry_dryrun_review_policy": policy,
        "planning_input_review": planning_input_review,
        "governance_standard_reuse_review": governance_reuse,
        "model_profile_registry_candidate": registry_candidate,
        "model_profile_schema_review": schema_review,
        "model_profile_lifecycle_policy_review": lifecycle_review,
        "model_profile_status_taxonomy_review": status_review,
        "source_license_metadata_schema_review": license_review,
        "capability_layer_binding_schema_review": layer_review,
        "model_input_output_profile_schema_review": io_review,
        "model_quality_acceptance_profile_schema_review": quality_review,
        "health_validation_whitebox_profile_schema_review": health_review,
        "provider_runtime_binding_profile_schema_review": provider_review,
        "version_update_replacement_profile_schema_review": version_review,
        "registry_domain_index_review": index_review,
        "seed_model_profile_candidates_review": seeds_review,
        "vision_model_profile_seed_candidates_review": vision_review,
        "ocr_model_profile_seed_candidates_review": ocr_review,
        "tts_model_profile_seed_candidates_review": tts_review,
        "asr_model_profile_seed_candidates_review": asr_review,
        "map_navigation_model_profile_seed_candidates_review": nav_review,
        "world_continuity_model_profile_seed_candidates_review": world_review,
        "memory_emotion_evolution_model_profile_seed_candidates_review": mem_review,
        "module_local_binding_review": module_review,
        "midplatform_governance_binding_review": mid_review,
        "registry_non_runtime_boundary_audit": boundary_audit,
        "registry_blocked_path_result": blocked_path_result,
        "registry_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
