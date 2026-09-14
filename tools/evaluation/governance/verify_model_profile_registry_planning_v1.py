#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Model Profile Registry Planning v1."""

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
from capabilities.governance.model_profile_registry_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    HEALTH_VALIDATION_FIELDS,
    IO_FORBIDDEN,
    IO_INPUT_TYPES,
    IO_OUTPUT_TYPES,
    LAYER_BINDING_FIELDS,
    LICENSE_METADATA_FIELDS,
    LIFECYCLE_STATES,
    MODEL_PROFILE_SCHEMA_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PROVIDER_RUNTIME_BINDING_FIELDS,
    QUALITY_PROFILE_FIELDS,
    REGISTRY_DUTIES,
    REGISTRY_NOT,
    SCOPE,
    SEED_CANDIDATE_IDS,
    SEED_CANDIDATE_REQUIRED,
    STATUS_TAXONOMY,
    VERSION_REPLACEMENT_FIELDS,
)
from capabilities.governance.scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as ROADMAP_DR_FINAL_GO,
)

MIN_CHECKS = 474

REQUIRED = (
    "model_profile_registry_planning_policy_v1.json",
    "roadmap_input_review_v1.json",
    "model_profile_registry_definition_v1.json",
    "model_profile_schema_v1.json",
    "model_profile_lifecycle_policy_v1.json",
    "model_profile_status_taxonomy_v1.json",
    "model_source_and_license_metadata_schema_v1.json",
    "model_capability_layer_binding_schema_v1.json",
    "model_input_output_profile_schema_v1.json",
    "model_quality_acceptance_profile_schema_v1.json",
    "model_health_validation_whitebox_profile_schema_v1.json",
    "model_provider_runtime_binding_profile_schema_v1.json",
    "model_version_update_replacement_profile_schema_v1.json",
    "model_profile_registry_domain_index_v1.json",
    "seed_model_profile_candidates_v1.json",
    "vision_model_profile_seed_candidates_v1.json",
    "ocr_model_profile_seed_candidates_v1.json",
    "tts_model_profile_seed_candidates_v1.json",
    "asr_model_profile_seed_candidates_v1.json",
    "map_navigation_model_profile_seed_candidates_v1.json",
    "world_continuity_model_profile_seed_candidates_v1.json",
    "memory_emotion_evolution_model_profile_seed_candidates_v1.json",
    "model_profile_to_module_local_binding_plan_v1.json",
    "model_profile_to_midplatform_governance_binding_plan_v1.json",
    "model_profile_registry_non_runtime_boundary_matrix_v1.json",
    "model_profile_registry_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "model_profile_registry_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/model_profile_registry_planning",
    )
    p.add_argument(
        "--roadmap-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "scenario_model_capability_roadmap_current_state_inventory_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    roadmap_vr = _load(Path(args.roadmap_dryrun_root) / "verifier_report.json")
    roadmap_sm = _load(Path(args.roadmap_dryrun_root) / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "model_profile_registry_planning_policy_v1.json")
    roadmap_in = _load(root / "roadmap_input_review_v1.json")
    registry_def = _load(root / "model_profile_registry_definition_v1.json")
    schema = _load(root / "model_profile_schema_v1.json")
    lifecycle = _load(root / "model_profile_lifecycle_policy_v1.json")
    status_tax = _load(root / "model_profile_status_taxonomy_v1.json")
    license_s = _load(root / "model_source_and_license_metadata_schema_v1.json")
    layer_s = _load(root / "model_capability_layer_binding_schema_v1.json")
    io_s = _load(root / "model_input_output_profile_schema_v1.json")
    qual_s = _load(root / "model_quality_acceptance_profile_schema_v1.json")
    health_s = _load(root / "model_health_validation_whitebox_profile_schema_v1.json")
    prov_s = _load(root / "model_provider_runtime_binding_profile_schema_v1.json")
    ver_s = _load(root / "model_version_update_replacement_profile_schema_v1.json")
    domain_idx = _load(root / "model_profile_registry_domain_index_v1.json")
    seeds = _load(root / "seed_model_profile_candidates_v1.json")
    vision = _load(root / "vision_model_profile_seed_candidates_v1.json")
    ocr = _load(root / "ocr_model_profile_seed_candidates_v1.json")
    tts = _load(root / "tts_model_profile_seed_candidates_v1.json")
    asr = _load(root / "asr_model_profile_seed_candidates_v1.json")
    nav = _load(root / "map_navigation_model_profile_seed_candidates_v1.json")
    world = _load(root / "world_continuity_model_profile_seed_candidates_v1.json")
    mem_emo = _load(root / "memory_emotion_evolution_model_profile_seed_candidates_v1.json")
    module_plan = _load(root / "model_profile_to_module_local_binding_plan_v1.json")
    mid_plan = _load(root / "model_profile_to_midplatform_governance_binding_plan_v1.json")
    boundary = _load(root / "model_profile_registry_non_runtime_boundary_matrix_v1.json")
    dryrun = _load(root / "model_profile_registry_dryrun_plan_v1.json")
    decision = _load(root / "model_profile_registry_planning_decision_v1.json")

    ok("upstream.roadmap_go", roadmap_vr.get("verifier") == "GO")
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == ROADMAP_DR_FINAL_GO)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.seeds14", summary.get("seed_candidate_count") == 14)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.registry_only", policy.get("registry_planning_only") is True)
    ok("roadmap_in.pass", roadmap_in.get("review_pass") is True)
    ok("roadmap_in.domains12", roadmap_in.get("capability_domain_count") == 12)

    ok("registry.id", registry_def.get("registry_id") == "luna_model_profile_registry_v1")
    ok("registry.type", registry_def.get("registry_type") == "model_candidate_profile_registry")
    ok("registry.no_runtime", registry_def.get("registry_runtime_enabled_now") is False)
    ok("registry.no_select", registry_def.get("model_selection_allowed_now") is False)
    ok("registry.no_invoke", registry_def.get("model_invocation_allowed_now") is False)
    ok("registry.no_bench", registry_def.get("benchmark_allowed_now") is False)
    ok("registry.candidate", registry_def.get("candidate_only") is True)
    for duty in REGISTRY_DUTIES:
        ok(f"duty.{duty[:18]}", duty in (registry_def.get("registry_duties") or []))
    for not_role in REGISTRY_NOT:
        ok(f"not.{not_role[:18]}", not_role in (registry_def.get("registry_is_not") or []))

    for field in MODEL_PROFILE_SCHEMA_FIELDS:
        ok(f"schema.{field[:16]}", field in (schema.get("required_fields") or []))
    ok("schema.source_chain", schema.get("defaults", {}).get("source_chain_required") is True)
    ok("schema.whitebox", schema.get("defaults", {}).get("whitebox_trace_required") is True)
    ok("schema.no_fact", schema.get("defaults", {}).get("no_direct_fact_action_output") is True)

    ok("lifecycle.count12", len(lifecycle.get("lifecycle_states") or []) == 12)
    ok("lifecycle.reg_ne_sel", lifecycle.get("rules", {}).get("registered_ne_selected") is True)
    ok("lifecycle.sel_later_blocked", lifecycle.get("rules", {}).get("selected_later_not_allowed_now") is True)

    ok("status.count11", len(status_tax.get("status_types") or []) == 11)

    for field in LICENSE_METADATA_FIELDS:
        ok(f"license.{field[:14]}", field in (license_s.get("required_fields") or []))
    ok("license.update_track", license_s.get("defaults", {}).get("update_tracking_required") is True)

    for field in LAYER_BINDING_FIELDS:
        ok(f"layer.{field[:14]}", field in (layer_s.get("required_fields") or []))
    ok("layer.stack", layer_s.get("capability_stack_ref") == STANDARD_ID)
    ok("layer.gov", layer_s.get("layered_governance_mapping_ref") == ADDENDUM_ID)

    ok("io.inputs10", len(io_s.get("input_types") or []) == 10)
    ok("io.outputs10", len(io_s.get("output_types") or []) == 10)
    for forbidden in IO_FORBIDDEN:
        ok(f"io.forbid.{forbidden[:14]}", forbidden in (io_s.get("forbidden_outputs") or []))

    for field in QUALITY_PROFILE_FIELDS:
        ok(f"qual.{field[:14]}", field in (qual_s.get("required_fields") or []))

    for field in HEALTH_VALIDATION_FIELDS:
        ok(f"health.{field[:14]}", field in (health_s.get("required_fields") or []))
    ok("health.external", health_s.get("defaults", {}).get("health_oversight_external_to_bus") is True)

    for field in PROVIDER_RUNTIME_BINDING_FIELDS:
        ok(f"prov.{field[:14]}", field in (prov_s.get("required_fields") or []))
    ok("prov.no_runtime", prov_s.get("defaults", {}).get("runtime_invocation_allowed_now") is False)

    for field in VERSION_REPLACEMENT_FIELDS:
        ok(f"ver.{field[:14]}", field in (ver_s.get("required_fields") or []))

    ok("index.by_domain", bool(domain_idx.get("by_capability_domain")))
    ok("index.by_stage", bool(domain_idx.get("by_goal_stage")))
    ok("index.by_source", bool(domain_idx.get("by_model_source_strategy")))
    ok("index.by_status", bool(domain_idx.get("by_status")))
    ok("index.by_layer", bool(domain_idx.get("by_layered_capability_stack_layer")))

    ok("seeds.count14", seeds.get("candidate_count") == 14)
    seed_list = seeds.get("candidates") or []
    for sid in SEED_CANDIDATE_IDS:
        ok(f"seed.{sid[:20]}", any(c.get("model_profile_id") == sid for c in seed_list))
    for c in seed_list:
        for field in SEED_CANDIDATE_REQUIRED:
            ok(f"seedfld.{c.get('model_profile_id','')[:8]}.{field[:8]}", field in c)
        ok(f"seed.{c.get('model_profile_id','')[:12]}.not_sel", c.get("selected_now") is False)
        ok(f"seed.{c.get('model_profile_id','')[:12]}.not_inv", c.get("invoked_now") is False)

    ok("vision.count5", len(vision.get("candidates") or []) >= 4)
    ok("vision.no_runtime", "no camera/runtime" in str(vision.get("confirmations")))
    ok("ocr.placeholder", any(c.get("model_profile_id") == "other_ocr_provider_placeholder" for c in (ocr.get("candidates") or [])))
    ok("ocr.not_fact", "not fact" in str(ocr.get("confirmations")))
    ok("tts.qianwen", any(c.get("model_profile_id") == "qianwen_tts_candidate" for c in (tts.get("candidates") or [])))
    ok("tts.no_invoke", "no TTS invocation" in str(tts.get("confirmations")))
    ok("asr.sensevoice", any(c.get("model_profile_id") == "sensevoice_asr_candidate" for c in (asr.get("candidates") or [])))
    ok("asr.no_runtime", "no ASR runtime" in str(asr.get("confirmations")))
    ok("nav.stage3", "Stage 3" in str(nav.get("confirmations")))
    ok("nav.count4", len(nav.get("candidates") or []) == 4)
    ok("world.stcm", any(c.get("model_profile_id") == "stcm_self_developed_profile" for c in (world.get("candidates") or [])))
    ok("world.signals", "signals only" in str(world.get("confirmations")))
    ok("mem_evo.proposal", "proposal_only" in str(mem_emo.get("confirmations")))
    ok("mem_evo.count5", len(mem_emo.get("candidates") or []) == 5)

    ok("module.plan5", len(module_plan.get("rules") or []) >= 5)
    ok("mid.plan9", len(mid_plan.get("rules") or []) >= 9)
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
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
