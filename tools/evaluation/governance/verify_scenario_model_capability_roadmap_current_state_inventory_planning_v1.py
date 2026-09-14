#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Scenario Model Capability Roadmap and Current State Inventory Planning v1."""

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
from capabilities.governance.scenario_model_capability_roadmap_current_state_inventory_planning_v1 import (
    ASSET_STATUS_TYPES,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CAPABILITY_DOMAIN_IDS,
    DOMAIN_INVENTORY_FIELDS,
    EXTERNAL_CANDIDATE_REGISTER_FIELDS,
    FINAL_DECISION_GO,
    MIDPLATFORM_BINDING_FIELDS,
    MODEL_SOURCE_TYPES,
    MODULE_PROFILE_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    ROADMAP_RISKS,
    SCOPE,
)

MIN_CHECKS = 479

REQUIRED = (
    "scenario_model_capability_roadmap_inventory_policy_v1.json",
    "upstream_output_chain_input_review_v1.json",
    "luna_model_capability_roadmap_v1.json",
    "capability_domain_inventory_matrix_v1.json",
    "current_model_asset_inventory_v1.json",
    "goal_stage_to_capability_domain_matrix_v1.json",
    "capability_domain_roadmap_template_v1.json",
    "vision_scene_understanding_roadmap_v1.json",
    "ocr_text_reading_roadmap_v1.json",
    "tts_voice_output_roadmap_v1.json",
    "asr_voice_input_roadmap_v1.json",
    "map_navigation_roadmap_v1.json",
    "spatiotemporal_world_continuity_roadmap_v1.json",
    "memory_personal_continuity_roadmap_v1.json",
    "emotion_engine_roadmap_v1.json",
    "evolutionary_recursion_roadmap_v1.json",
    "provider_model_management_roadmap_v1.json",
    "model_source_strategy_taxonomy_v1.json",
    "external_open_source_candidate_register_v1.json",
    "reference_research_product_candidate_register_v1.json",
    "self_developed_core_capability_register_v1.json",
    "module_local_model_profile_contract_v1.json",
    "midplatform_model_governance_binding_contract_v1.json",
    "model_input_output_contract_standard_v1.json",
    "model_quality_acceptance_criteria_v1.json",
    "model_versioning_and_update_policy_v1.json",
    "model_replacement_and_fallback_policy_v1.json",
    "current_gap_and_next_action_matrix_v1.json",
    "roadmap_risk_register_v1.json",
    "roadmap_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "scenario_model_capability_roadmap_inventory_planning_decision_v1.json",
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
            "scenario_model_capability_roadmap_current_state_inventory_planning"
        ),
    )
    p.add_argument(
        "--closure-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "first_person_scene_understanding_output_chain_closure_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    closure_vr = _load(Path(args.closure_review_root) / "verifier_report.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "scenario_model_capability_roadmap_inventory_policy_v1.json")
    upstream = _load(root / "upstream_output_chain_input_review_v1.json")
    luna_roadmap = _load(root / "luna_model_capability_roadmap_v1.json")
    domain_matrix = _load(root / "capability_domain_inventory_matrix_v1.json")
    asset_inv = _load(root / "current_model_asset_inventory_v1.json")
    goal_matrix = _load(root / "goal_stage_to_capability_domain_matrix_v1.json")
    template = _load(root / "capability_domain_roadmap_template_v1.json")
    vision = _load(root / "vision_scene_understanding_roadmap_v1.json")
    ocr = _load(root / "ocr_text_reading_roadmap_v1.json")
    tts = _load(root / "tts_voice_output_roadmap_v1.json")
    asr = _load(root / "asr_voice_input_roadmap_v1.json")
    nav = _load(root / "map_navigation_roadmap_v1.json")
    st = _load(root / "spatiotemporal_world_continuity_roadmap_v1.json")
    memory = _load(root / "memory_personal_continuity_roadmap_v1.json")
    emotion = _load(root / "emotion_engine_roadmap_v1.json")
    evolution = _load(root / "evolutionary_recursion_roadmap_v1.json")
    provider = _load(root / "provider_model_management_roadmap_v1.json")
    external = _load(root / "external_open_source_candidate_register_v1.json")
    gap_matrix = _load(root / "current_gap_and_next_action_matrix_v1.json")
    module_contract = _load(root / "module_local_model_profile_contract_v1.json")
    mid_binding = _load(root / "midplatform_model_governance_binding_contract_v1.json")
    decision = _load(root / "scenario_model_capability_roadmap_inventory_planning_decision_v1.json")
    dryrun_plan = _load(root / "roadmap_dryrun_plan_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("upstream.closure_go", closure_vr.get("verifier") == "GO")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.domains12", summary.get("capability_domain_count") == 12)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.inventory_only", policy.get("roadmap_and_inventory_only") is True)
    ok("upstream.pass", upstream.get("review_pass") is True)

    ok("luna.product_roadmap", luna_roadmap.get("roadmap_type") == "product_development_roadmap_with_inventory")
    ok("luna.answers5", len(luna_roadmap.get("answers") or []) == 5)

    ok("domain_matrix.count12", domain_matrix.get("domain_count") == 12)
    for did in CAPABILITY_DOMAIN_IDS:
        dom = next((d for d in (domain_matrix.get("domains") or []) if d.get("capability_domain_id") == did), {})
        ok(f"domain.{did[:18]}", bool(dom))
        for field in DOMAIN_INVENTORY_FIELDS:
            ok(f"domain.{did[:8]}.{field[:10]}", field in dom)

    ok("asset.status_types7", len(asset_inv.get("status_types") or []) == len(ASSET_STATUS_TYPES))
    ok("asset.count15", len(asset_inv.get("assets") or []) >= 15)
    ok("asset.qianwen", any(a.get("asset_id") == "qianwen_tts_candidate" for a in (asset_inv.get("assets") or [])))
    ok("asset.asr_not_started", any(
        a.get("asset_id") == "asr_voice_input" and a.get("status") == "not_started"
        for a in (asset_inv.get("assets") or [])
    ))

    ok("goal_matrix.mappings", len(goal_matrix.get("mappings") or []) >= 6)
    ok("template.sections", template.get("section_count") == len(DOMAIN_INVENTORY_FIELDS))

    ok("vision.stage1", vision.get("current_goal_stage") == "stage_1")
    ok("vision.yolo", "yolo_family" in str(vision.get("candidate_model_sources")))
    ok("vision.gaps6", len(vision.get("current_gaps") or []) >= 6)
    ok("vision.next_profile", "Vision Module-local Model Profile" in str(vision.get("next_actions")))
    ok("vision.no_runtime", "不直接启 runtime" in str(vision.get("next_actions")))

    ok("ocr.candidate", "text_region_candidate" in str(ocr.get("first_stage_goal")))
    ok("ocr.paddle", "paddleocr" in str(ocr.get("candidate_model_sources")))
    ok("ocr.gap_runtime", any("runtime" in g for g in (ocr.get("current_gaps") or [])))

    ok("tts.qianwen", "qianwen" in str(tts.get("already_integrated_or_registered_models")))
    ok("tts.no_invoke", "not selected/invoked" in str(tts.get("actual_completion_status")))

    ok("asr.not_started", "尚未完整 runtime" in str(asr.get("actual_completion_status")))

    ok("nav.stage3", nav.get("current_goal_stage") == "stage_3")
    ok("nav.no_runtime", "未开启" in str(nav.get("actual_completion_status")))

    ok("st.self_dev", st.get("model_source_strategy") == "reference_inspired_rebuild")
    ok("st.not_single_model", "不能由单一外部模型替代" in str(st.get("version_update_replacement_notes")))

    ok("memory.self_dev", memory.get("model_source_strategy") == "self_developed_core_capability")
    ok("emotion.self_dev", emotion.get("model_source_strategy") == "self_developed_core_capability")
    ok("evolution.proposal", "proposal_only" in str(evolution.get("version_update_replacement_notes")))

    ok("provider.no_auto", "no auto-switch" in str(provider.get("first_stage_goal")))

    ok("external.register_only", external.get("register_only") is True)
    ok("external.candidates11", len(external.get("candidates") or []) >= 11)
    for c in external.get("candidates") or []:
        for field in EXTERNAL_CANDIDATE_REGISTER_FIELDS:
            ok(f"ext.{c.get('candidate_name','')[:10]}.{field[:8]}", field in c)

    ok("gap.entries12", len(gap_matrix.get("entries") or []) == 12)
    ok("gap.vision_p0", any(
        e.get("capability_domain_id") == "first_person_vision_scene_understanding" and e.get("priority") == "P0"
        for e in (gap_matrix.get("entries") or [])
    ))

    ok("module.fields", len(module_contract.get("required_fields") or []) == len(MODULE_PROFILE_FIELDS))
    ok("module.gov_ref", "layered_governance_mapping_ref" in MODULE_PROFILE_FIELDS)
    ok("mid.fields", len(mid_binding.get("required_fields") or []) == len(MIDPLATFORM_BINDING_FIELDS))
    ok("mid.stack", mid_binding.get("layered_stack_ref") == STANDARD_ID)
    ok("mid.gov", mid_binding.get("layered_governance_ref") == ADDENDUM_ID)

    for st in MODEL_SOURCE_TYPES:
        ok(f"source.{st[:12]}", st in MODEL_SOURCE_TYPES)

    for risk in ROADMAP_RISKS:
        ok(f"risk.{risk[:18]}", risk in (_load(root / "roadmap_risk_register_v1.json").get("risks") or []))

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (non_claims.get("non_claims") or []))

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
