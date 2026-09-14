# -*- coding: utf-8 -*-
"""Document Surface — Option B dependency admission dryrun v1."""

from __future__ import annotations

from typing import Any, Dict


def run_dependency_admission_dryrun(*, candidate: Dict[str, Any]) -> Dict[str, Any]:
    dep = candidate.get("dependency_profile") or {}
    controlled = dep.get("controlled", dep.get("type") == "python_builtin_or_existing" or dep.get("type") == "declared_only")
    if dep.get("type") == "runtime_binary_uncontrolled":
        return {
            "dependency_admission_result_candidate": "blocked_dependency_not_admitted_candidate",
            "install_allowed": False,
            "download_allowed": False,
            "execution_allowed": False,
            "network_access_allowed": False,
            "no_silent_install": True,
            "no_silent_download": True,
            "failure_output": "dependency_not_admitted_candidate",
            "candidate_only": True,
            "not_fact": True,
        }
    if dep.get("type") == "hardware_requirement" and dep.get("available") is False:
        return {
            "dependency_admission_result_candidate": "blocked_hardware_requirement_missing_candidate",
            "install_allowed": False,
            "download_allowed": False,
            "execution_allowed": False,
            "network_access_allowed": False,
            "no_silent_install": True,
            "no_silent_download": True,
            "failure_output": "hardware_requirement_missing_candidate",
            "candidate_only": True,
            "not_fact": True,
        }
    return {
        "dependency_admission_result_candidate": "dependency_admission_passed_candidate" if controlled else "blocked_dependency_not_admitted_candidate",
        "install_allowed": False,
        "download_allowed": False,
        "execution_allowed": False,
        "network_access_allowed": False,
        "no_silent_install": True,
        "no_silent_download": True,
        "failure_output": None if controlled else "dependency_not_admitted_candidate",
        "candidate_only": True,
        "not_fact": True,
    }
