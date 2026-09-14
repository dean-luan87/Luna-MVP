# -*- coding: utf-8 -*-
"""Document Surface — Option B preflight post-review adapter (closure) v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

POST_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_PREFLIGHT_POST_REVIEW_GO"
POST_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_PREFLIGHT_POST_REVIEW_BLOCKED"
NEXT_CE_PLANNING = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Controlled-Execution-Planning-v1-001"

PERSISTENT_RISKS = [
    "option_b_specific_real_model_not_selected",
    "option_b_preflight_not_executed",
    "option_b_segmentation_quality_unknown",
    "wrapper_contract_not_implemented",
    "controlled_execution_not_started",
    "option_a_limitations_remain",
    "field_centric_role_dryrun_pending",
]


def run_preflight_post_review_substage(
    *,
    planning: Dict[str, Any],
    dryrun: Dict[str, Any],
    metrics: Dict[str, Any],
    repo_root: Path,
) -> Dict[str, Any]:
    blockers: List[str] = []
    if not planning.get("passed"):
        blockers.append("planning.failed")
    if not dryrun.get("passed"):
        blockers.append("dryrun.failed")
    scope = dryrun.get("scope_results") or {}
    if scope.get("preflight_candidate_count") != 2:
        blockers.append("scope.count")
    if metrics.get("execution_allowed_rate", 1) != 0:
        blockers.append("metrics.execution")
    if metrics.get("active_registry_update_rate", 1) != 0:
        blockers.append("metrics.registry")

    chain_path = repo_root / "capabilities/midplatform/protocols/region_intelligence_protocol_chain_v1.json"
    chain_ok = False
    if chain_path.is_file():
        chain = json.loads(chain_path.read_text(encoding="utf-8"))
        refs = [p.get("protocol_ref") for p in chain.get("legacy_protocols_required") or []]
        chain_ok = "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1" in refs
    if not chain_ok:
        blockers.append("protocol.chain")

    decision = POST_GO if not blockers else POST_BLOCKED
    return {
        "substage": "preflight_post_review",
        "preflight_post_review_decision": decision,
        "passed": decision == POST_GO,
        "blockers": blockers,
        "recommended_next_phase": NEXT_CE_PLANNING if decision == POST_GO else None,
        "risk_registry": {
            "mitigated_risks": [
                "preflight_checklist_planned",
                "preflight_dryrun_validated",
                "preflight_abort_rollback_defined",
                "no_preflight_execution_in_closure",
            ],
            "unresolved_risks": PERSISTENT_RISKS,
        },
        "summary": {
            "phase_id": "Phase-P1-...-OptionB-Preflight-Post-Review-v1-001",
            "post_review_only": True,
            "preflight_execution_allowed": False,
            "option_b_execution_allowed": False,
            "final_decision": decision,
            "recommended_next_phase": NEXT_CE_PLANNING if decision == POST_GO else None,
            "candidate_only": True,
            "not_fact": True,
        },
        "candidate_only": True,
        "not_fact": True,
    }
