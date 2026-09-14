# -*- coding: utf-8 -*-
"""Vision / Voice Provider Harness Adoption DryRun v1 — harness consumes domain_config."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.controlled_provider_readiness_harness_v1 import (
    ANTI_RECURSION,
    HARNESS_ID,
    HARNESS_PHASES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.vision_voice_provider_harness_adoption_planning_v1 import (
    ADOPTION_BLOCKED_PATHS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    HARNESS_SUB_CONTRACTS,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    VISION_CANDIDATES,
    VISION_FAILURE_ROUTES,
    VOICE_CANDIDATES,
    VOICE_FAILURE_ROUTES,
)

PHASE_ID = "Phase-Vision-Voice-Provider-Harness-Adoption-DryRun-v1-001"
SCOPE = "vision_voice_provider_harness_adoption_dryrun_only"
SOURCE_CHAIN = "vision_voice_provider_harness_adoption_dryrun_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = "VISION_VOICE_PROVIDER_HARNESS_ADOPTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "VISION_VOICE_PROVIDER_HARNESS_ADOPTION_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Vision-Voice-Provider-Harness-Adoption-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-Vision-Voice-Provider-Harness-Adoption-Issue-Review-v1-001"

NON_CLAIMS: Tuple[str, ...] = (
    "DryRun GO ≠ Vision/Voice provider runtime enabled",
    "readiness candidate ≠ provider authorized",
    "harness consumption simulated ≠ harness globally enforced",
    "Post-DryRun Review next ≠ live camera or ASR/TTS",
    "generalization pass ≠ Map/Library/Hive runtime enabled",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "harness_adoption_execution_started_now",
    "harness_runtime_enforced_globally_now",
    "provider_runtime_enabled_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "real_vision_model_invoked_now",
    "live_camera_enabled_now",
    "image_read_executed_now",
    "asr_runtime_invoked_now",
    "tts_runtime_invoked_now",
    "voice_output_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/vision_voice_provider_harness_adoption_dryrun"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "vision_voice_provider_harness_adoption_dryrun_only": True,
        "simulated": True,
        "vision_provider_readiness_candidate_generated_now": True,
        "voice_provider_readiness_candidate_generated_now": True,
        "harness_id": HARNESS_ID,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _contract_consumption_matrix(domain: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    rows = [
        {
            "sub_contract": contract,
            "mapped": True,
            "domain_specific_required_fields_satisfied": True,
            "ocr_specific_fields_required": False,
            "consumer_domain": domain,
        }
        for contract in HARNESS_SUB_CONTRACTS
    ]
    return {
        "matrix_id": f"{domain}_harness_contract_consumption_matrix_v1",
        "provider_domain": domain,
        "harness_id": HARNESS_ID,
        "rows": rows,
        "row_count": len(rows),
        "all_mapped": True,
        **meta,
    }


def _readiness_candidate(
    *,
    domain: str,
    candidates: Tuple[Dict[str, Any], ...],
    domain_plan: Dict[str, Any],
    meta: Dict[str, Any],
) -> Dict[str, Any]:
    enriched = []
    defaults = domain_plan.get("defaults") or {}
    for c in candidates:
        enriched.append(
            {
                **c,
                **defaults,
                "candidate_type": "provider_readiness_candidate",
                "harness_consumed": True,
                "simulated": True,
            }
        )
    out: Dict[str, Any] = {
        "artifact_id": f"{domain}_provider_readiness_candidate_v1",
        "provider_domain": domain,
        "candidates": enriched,
        "candidate_count": len(enriched),
        "harness_id": HARNESS_ID,
        "harness_phases_covered": list(HARNESS_PHASES),
        **meta,
    }
    if domain == "vision":
        out["output_contract"] = domain_plan.get("output_contract")
        out["evidence_pack"] = domain_plan.get("evidence_pack")
        out["live_camera_allowed"] = defaults.get("live_camera_allowed", False)
        out["image_read_allowed"] = defaults.get("image_read_allowed", False)
    else:
        out["output_contracts"] = domain_plan.get("output_contracts")
        out["evidence_pack"] = domain_plan.get("evidence_pack")
        out["asr_runtime_allowed"] = defaults.get("asr_runtime_allowed", False)
        out["tts_runtime_allowed"] = defaults.get("tts_runtime_allowed", False)
        out["voice_output_allowed"] = defaults.get("voice_output_allowed", False)
    return out


def run_vision_voice_provider_harness_adoption_dryrun_v1(
    *,
    vision_voice_provider_harness_adoption_planning_root: str,
    controlled_provider_readiness_harness_root: Optional[str] = None,
    ocr_provider_next_roadmap_decision_root: Optional[str] = None,
    vision_ocr_voice_controlled_optimization_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(vision_voice_provider_harness_adoption_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    gen_review = _try_read_json(
        planning_root / "future_harness_consumer_generalization_review_v1.json"
    ) or {}
    vision_domain_plan = _try_read_json(planning_root / "vision_provider_domain_config_plan_v1.json") or {}
    voice_domain_plan = _try_read_json(planning_root / "voice_provider_domain_config_plan_v1.json") or {}
    boundary_plan = _try_read_json(planning_root / "vision_voice_adoption_boundary_matrix_v1.json") or {}

    harness_root = Path(
        controlled_provider_readiness_harness_root
        or planning_root.parent / "controlled_provider_readiness_harness"
    ).expanduser().resolve()
    harness_sm = _try_read_json(harness_root / "summary.json") or {}
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}
    validation = _try_read_json(
        harness_root / "controlled_provider_readiness_harness_validation_result_v1.json"
    ) or {}

    roadmap_root = Path(
        ocr_provider_next_roadmap_decision_root
        or planning_root.parent / "ocr_provider_next_roadmap_decision"
    ).expanduser().resolve()
    vov_post_root = Path(
        vision_ocr_voice_controlled_optimization_post_dryrun_review_root
        or planning_root.parent / "vision_ocr_voice_controlled_optimization_post_dryrun_review"
    ).expanduser().resolve()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(planning_root),
        "upstream_harness_root": str(harness_root),
        "output_root": str(out_root),
    }

    planning_go = plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True
    if not planning_go:
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if gen_review.get("vision_second_consumer_mappable") is not True:
        blockers.append("vision_second_consumer_mappable required")
    if gen_review.get("voice_third_consumer_mappable") is not True:
        blockers.append("voice_third_consumer_mappable required")
    if gen_review.get("no_ocr_specific_fields_leak_into_vision_voice_required_contract") is not True:
        blockers.append("ocr_specific_fields_not_required must be true")

    if harness_vr.get("verifier") != "GO":
        blockers.append("harness verifier should be GO")
    if validation.get("ocr_first_consumer_validated") is not True:
        blockers.append("OCR first consumer must be validated")
    if harness_sm.get("harness_runtime_enforced_globally_now") is True:
        blockers.append("harness_runtime_enforced_globally_now must be false")

    if boundary_plan.get("all_blocked") is not True:
        blockers.append("planning blocked paths must be all blocked")

    vov_sm = _try_read_json(vov_post_root / "summary.json") or {}
    if vov_sm.get("controlled_optimization_dryrun_closed") is not True:
        blockers.append("vov controlled optimization should be closed")

    input_review = {
        "review_id": "vision_voice_harness_adoption_planning_input_review_v1",
        "upstream_planning_root": str(planning_root),
        "upstream_harness_root": str(harness_root),
        "upstream_verifier_go": planning_go,
        "upstream_final_decision": plan_sm.get("final_decision"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    vision_consumption = {
        "result_id": "vision_domain_config_consumption_result_v1",
        "harness_id": HARNESS_ID,
        "domain_config_source": str(planning_root / "vision_provider_domain_config_plan_v1.json"),
        "consumed": True,
        "consumer_order": "second",
        "ocr_specific_fields_required": False,
        **meta,
    }

    voice_consumption = {
        "result_id": "voice_domain_config_consumption_result_v1",
        "harness_id": HARNESS_ID,
        "domain_config_source": str(planning_root / "voice_provider_domain_config_plan_v1.json"),
        "consumed": True,
        "consumer_order": "third",
        "ocr_specific_fields_required": False,
        **meta,
    }

    vision_readiness = _readiness_candidate(
        domain="vision",
        candidates=VISION_CANDIDATES,
        domain_plan=vision_domain_plan,
        meta=meta,
    )
    voice_readiness = _readiness_candidate(
        domain="voice",
        candidates=VOICE_CANDIDATES,
        domain_plan=voice_domain_plan,
        meta=meta,
    )

    vision_contract_matrix = _contract_consumption_matrix("vision", meta)
    voice_contract_matrix = _contract_consumption_matrix("voice", meta)

    vision_failure = {
        "result_id": "vision_failure_route_dryrun_result_v1",
        "routes": [
            {**r, "routed": True, "executed_now": False, "candidate_only": True}
            for r in VISION_FAILURE_ROUTES
        ],
        "route_count": len(VISION_FAILURE_ROUTES),
        **meta,
    }

    voice_failure = {
        "result_id": "voice_failure_route_dryrun_result_v1",
        "routes": [
            {**r, "routed": True, "executed_now": False, "candidate_only": True}
            for r in VOICE_FAILURE_ROUTES
        ],
        "route_count": len(VOICE_FAILURE_ROUTES),
        **meta,
    }

    boundary_guard = {
        "result_id": "vision_voice_boundary_guard_dryrun_result_v1",
        "paths": [{"path_id": p, "blocked": True} for p in ADOPTION_BLOCKED_PATHS],
        "path_count": len(ADOPTION_BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    harness_contract_doc = _try_read_json(
        harness_root / "controlled_provider_readiness_harness_contract_v1.json"
    ) or {}
    anti_rules = harness_contract_doc.get("anti_recursion_rules") or []

    generalization = {
        "result_id": "harness_generalization_dryrun_result_v1",
        "ocr_first_consumer_validated": validation.get("ocr_first_consumer_validated"),
        "vision_second_consumer_dryrun_pass": len(blockers) == 0,
        "voice_third_consumer_dryrun_pass": len(blockers) == 0,
        "map_library_hive_memory_future_only": True,
        "no_automatic_consumer_runtime_enablement": True,
        "no_ocr_specific_fields_leak": gen_review.get(
            "no_ocr_specific_fields_leak_into_vision_voice_required_contract"
        ),
        "domain_config_required": True,
        "anti_recursion_preserved": len(anti_rules) >= len(ANTI_RECURSION),
        "generalization_pass": len(blockers) == 0,
        **meta,
    }

    no_runtime_audit = {
        "audit_id": "vision_voice_no_runtime_audit_v1",
        "real_vision_model_invoked_now": False,
        "live_camera_enabled_now": False,
        "image_read_executed_now": False,
        "asr_runtime_invoked_now": False,
        "tts_runtime_invoked_now": False,
        "voice_output_generated_now": False,
        "provider_imported_now": False,
        "harness_adoption_execution_started_now": False,
        "audit_pass": True,
        **meta,
    }

    blocked_result = {
        "result_id": "vision_voice_harness_adoption_blocked_path_result_v1",
        "paths": boundary_guard["paths"],
        "path_count": boundary_guard["path_count"],
        "all_blocked": True,
        **meta,
    }

    checks_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and vision_consumption.get("consumed")
        and voice_consumption.get("consumed")
        and vision_readiness.get("candidate_count") == 4
        and voice_readiness.get("candidate_count") == 5
        and vision_contract_matrix.get("all_mapped")
        and voice_contract_matrix.get("all_mapped")
        and boundary_guard.get("all_blocked")
        and no_runtime_audit.get("audit_pass")
        and generalization.get("generalization_pass")
    )

    readiness = {
        "decision_id": "vision_voice_harness_adoption_readiness_decision_v1",
        "vision_pass": checks_pass,
        "voice_pass": checks_pass,
        "contract_consumption_pass": checks_pass,
        "boundary_pass": checks_pass,
        "generalization_pass": checks_pass,
        "all_pass": checks_pass,
        "high_risk_count": 0 if checks_pass else 1,
        "final_decision": FINAL_DECISION_GO if checks_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if checks_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "vision_voice_harness_adoption_dryrun_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
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
        "boundary_ok": checks_pass,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        **meta,
    }

    return {
        "vision_voice_harness_adoption_dryrun_policy": policy,
        "vision_voice_harness_adoption_planning_input_review": input_review,
        "vision_domain_config_consumption_result": vision_consumption,
        "voice_domain_config_consumption_result": voice_consumption,
        "vision_provider_readiness_candidate": vision_readiness,
        "voice_provider_readiness_candidate": voice_readiness,
        "vision_harness_contract_consumption_matrix": vision_contract_matrix,
        "voice_harness_contract_consumption_matrix": voice_contract_matrix,
        "vision_failure_route_dryrun_result": vision_failure,
        "voice_failure_route_dryrun_result": voice_failure,
        "vision_voice_boundary_guard_dryrun_result": boundary_guard,
        "harness_generalization_dryrun_result": generalization,
        "vision_voice_no_runtime_audit": no_runtime_audit,
        "vision_voice_harness_adoption_blocked_path_result": blocked_result,
        "vision_voice_harness_adoption_readiness_decision": readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
