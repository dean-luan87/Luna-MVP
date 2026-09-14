# -*- coding: utf-8 -*-
"""Document Surface — Option B permission admission mapping dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List


def run_permission_admission_mapping_dryrun(*, dependency_mapping: Dict[str, Any]) -> Dict[str, Any]:
    records = dependency_mapping.get("records") or []
    return {
        "dryrun_id": "option_b_permission_admission_mapping_dryrun_v1",
        "permission_contract": "Permission / Admission Contract",
        "records": [
            {
                "model_candidate_id": r.get("model_candidate_id"),
                "permission_status": r.get("permission_mapping"),
                "install_denied": r.get("install_allowed") is False,
                "download_denied": r.get("download_allowed") is False,
                "execution_denied": r.get("execution_allowed") is False,
                "network_denied": r.get("network_access_allowed") is False,
            }
            for r in records
        ],
        "permission_denial_mapping_complete": dependency_mapping.get("permission_denied_count", 0) >= 4,
        "no_permission_escalation": (
            dependency_mapping.get("no_install_escalation") is True
            and dependency_mapping.get("no_execution_escalation") is True
        ),
        "candidate_only": True,
        "not_fact": True,
    }
