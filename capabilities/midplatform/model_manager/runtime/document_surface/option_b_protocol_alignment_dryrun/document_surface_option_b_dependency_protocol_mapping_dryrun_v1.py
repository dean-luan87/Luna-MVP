# -*- coding: utf-8 -*-
"""Document Surface — Option B dependency protocol mapping dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List

PERMISSION_DENIED_STATUSES = frozenset({
    "blocked_dependency_not_admitted_candidate",
    "blocked_model_weight_missing_candidate",
    "blocked_license_not_cleared_candidate",
    "blocked_hardware_requirement_missing_candidate",
})


def run_dependency_protocol_mapping_dryrun(*, admission_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    per: List[Dict[str, Any]] = []
    for r in admission_results:
        status = r.get("admission_status_candidate", "")
        dep = r.get("dependency_admission") or {}
        lic = r.get("license_weight") or {}
        denied = status in PERMISSION_DENIED_STATUSES
        per.append({
            "model_candidate_id": r["model_candidate_id"],
            "admission_status_candidate": status,
            "permission_mapping": "permission_denied_candidate" if denied else "permission_not_granted_preflight_only",
            "install_allowed": dep.get("install_allowed", False),
            "download_allowed": dep.get("download_allowed", False),
            "execution_allowed": dep.get("execution_allowed", False),
            "network_access_allowed": dep.get("network_access_allowed", False),
            "no_silent_install": dep.get("no_silent_install", True),
            "no_silent_download": dep.get("no_silent_download", True),
            "license_blocked": "license" in status,
            "weight_blocked": "weight" in status,
            "hardware_blocked": "hardware" in status,
            "dependency_blocked": "dependency" in status,
        })
    denied_count = sum(1 for p in per if p["permission_mapping"] == "permission_denied_candidate")
    return {
        "dryrun_id": "option_b_dependency_protocol_mapping_dryrun_v1",
        "permission_contract": "Permission / Admission Contract",
        "records": per,
        "permission_denied_count": denied_count,
        "no_install_escalation": all(p.get("install_allowed") is False for p in per),
        "no_download_escalation": all(p.get("download_allowed") is False for p in per),
        "no_execution_escalation": all(p.get("execution_allowed") is False for p in per),
        "candidate_only": True,
        "not_fact": True,
    }
