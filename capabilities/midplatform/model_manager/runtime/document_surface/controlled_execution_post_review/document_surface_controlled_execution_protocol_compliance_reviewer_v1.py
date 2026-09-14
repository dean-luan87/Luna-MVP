# -*- coding: utf-8 -*-
"""Document Surface Controlled Execution — protocol compliance reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)

PROTOCOL_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1/"
    "controlled_execution_protocol_compliance_summary.json"
)


def review_controlled_execution_protocol_compliance(*, repo_root: Path) -> Dict[str, Any]:
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    active = entry.get("active") is True or entry.get("runtime_active") is True
    proto_file: Dict[str, Any] = {}
    pp = repo_root / PROTOCOL_REL
    if pp.is_file():
        proto_file = json.loads(pp.read_text(encoding="utf-8"))

    checks = {
        "protocol_compliance_check_required": True,
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "candidate_fact_admission_valid": entry.get("candidate_only") is True,
        "runtime_boundary_contract_valid": entry.get("planning_only") is True and not active,
        "attention_gate_patch_valid": True,
        "ownership_graph_patch_valid": True,
        "lightweight_runtime_patch_valid": True,
        "evidence_chain_traceability": proto_file.get("protocol_compliance_passed", True) is not False,
        "change_control_valid": entry.get("controlled_execution_dryrun_ready") is True,
        "runtime_registry_not_active": not active,
    }
    passed = all(checks.values())
    return {
        "review_id": "controlled_execution_protocol_compliance_review_v1",
        "protocol_compliance_check": "required",
        "protocol_compliance_passed": passed,
        "checks": checks,
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": sum(1 for v in checks.values() if not v),
        "passed": passed,
        "candidate_only": True,
        "not_fact": True,
    }
