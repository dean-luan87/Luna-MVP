# -*- coding: utf-8 -*-
"""Document Surface — Option B dependency admission protocol mapping v1."""

from __future__ import annotations

from typing import Any, Dict, List


def build_dependency_admission_protocol_mapping(*, dependency_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    per: List[Dict[str, Any]] = []
    for i, dep in enumerate(dependency_results):
        per.append({
            "index": i,
            "dependency_admission_result_candidate": dep.get("dependency_admission_result_candidate"),
            "permission_contract_gates": {
                "install_allowed": dep.get("install_allowed"),
                "download_allowed": dep.get("download_allowed"),
                "execution_allowed": dep.get("execution_allowed"),
                "network_access_allowed": dep.get("network_access_allowed"),
            },
            "no_silent_install": dep.get("no_silent_install"),
            "no_silent_download": dep.get("no_silent_download"),
            "aligned_to_permission_admission_contract": (
                dep.get("install_allowed") is False
                and dep.get("download_allowed") is False
                and dep.get("execution_allowed") is False
            ),
        })
    return {
        "mapping_id": "option_b_dependency_admission_protocol_mapping_v1",
        "permission_contract": "Permission / Admission Contract",
        "all_install_blocked": all(d.get("install_allowed") is False for d in dependency_results),
        "all_download_blocked": all(d.get("download_allowed") is False for d in dependency_results),
        "all_execution_blocked": all(d.get("execution_allowed") is False for d in dependency_results),
        "per_result": per,
        "candidate_only": True,
        "not_fact": True,
    }
